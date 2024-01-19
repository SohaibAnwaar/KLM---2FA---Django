from datetime import timezone, datetime
from io import BytesIO

import pyotp
import qrcode
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account import app_settings as allauth_account_settings
from allauth.account.utils import setup_user_email
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.files.base import ContentFile
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from klm.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "name", "email", "username", "created_at"]


class CustomRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=True, validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    qr_code = serializers.ImageField(read_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        user.name = self.cleaned_data["name"]
        # create totp and qr for the user
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=self.cleaned_data["email"].lower(), issuer_name="KLM"
        )
        stream = BytesIO()
        image = qrcode.make(f"{otp_auth_url}")
        image.save(stream)

        user.otp_base32 = otp_base32
        user.otpauth_url = otp_auth_url
        user.qr_code = ContentFile(stream.getvalue(), name="qrcode.png")
        user.save()
        return user

    def get_cleaned_data(self):
        return {
            "name": self.validated_data.get('name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user = self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user, email=None):
        if not user.emailaddress_set.filter(email=user.email, verified=True).exists():
            raise serializers.ValidationError(_('E-mail is not verified.'))

    def validate(self, attrs: dict):
        username = attrs.get("username")
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # check if the user is active
        self.validate_auth_user_status(user)

        # is the email verified?
        self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs

    def create(self, validated_data: dict):
        user: User = validated_data.get("user")
        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    user_id = serializers.UUIDField()

    def validate(self, attrs: dict):
        user: User = User.objects.filter(pk=attrs.get("user_id")).first()
        if not user:
            raise exceptions.AuthenticationFailed("User Not found.")

        totp = pyotp.TOTP(user.otp_base32).now()
        if attrs.get("otp") != totp:
            raise exceptions.AuthenticationFailed("Authentication Failed.")
        attrs["user"] = user
        return super().validate(attrs)

    def create(self, validated_data: dict):
        user: User = validated_data.get("user")
        refresh = RefreshToken.for_user(user)
        user.login_otp_used = True
        user.save(update_fields=["login_otp_used"])
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

