import os
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from klm.common.models import CoreModel
from klm.users.managers import UserManager


def get_qr_code_file_path(instance, filename):
    # Generate the path based on user ID and filename "qrcode.png"
    datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{datetime_str}sqr_code.png"
    return os.path.join(
        str(instance.uuid),
        "images",
        filename
    )


class User(CoreModel, AbstractUser):
    """
    Default custom user model for KLM Project.
    """
    # First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    otpauth_url = models.CharField(max_length=225, blank=True, null=True)
    otp_base32 = models.CharField(max_length=255, null=True)
    qr_code = models.ImageField(upload_to=get_qr_code_file_path, blank=True, null=True)
    login_otp = models.CharField(max_length=255, null=True, blank=True)
    login_otp_used = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.email

    @property
    def get_full_name(self) -> str:
        return self.name
