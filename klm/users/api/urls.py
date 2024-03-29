from dj_rest_auth.registration.views import (
    ResendEmailVerificationView, VerifyEmailView
)
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView
)
from klm.users.api.views import (email_confirm_redirect, password_reset_confirm_redirect, LoginView, VerityOTPView,
                                 )
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import UserDetailsView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("verify-otp/", VerityOTPView.as_view(), name="verify-otp"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("me/", UserDetailsView.as_view(), name="rest_user_details"),
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path("register/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

]
