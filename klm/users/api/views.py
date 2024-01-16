from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework import generics, permissions
from rest_framework.response import Response

from klm.users.api.serializers import LoginSerializer


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class LoginView(generics.GenericAPIView):
    """Login with email and password"""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "user": user.pk,
                "qr_code": user.qr_code.url,
                "message": "Login Successful. Proceed to 2FA",
            },
            status=200,
        )


# class VerityOTPView(generics.GenericAPIView):
#     """
#
#     """
#     serializer_class = VerifyOTPSerializer
#
#     def post(self, request, format=None):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         login_info: dict = serializer.save()
#         return Response(login_info,status=200)