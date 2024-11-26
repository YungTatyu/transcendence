from django.urls import path
from .views import (
    otp_generate,
    otp_verify,
    otp_resend,
    login,
    login_otp_verify,
    login_otp_resend,
)


urlpatterns = [
    # path("signup/", signup),
    path("otp/generate/", otp_generate),
    path("otp/verify/", otp_verify),
    path("otp/resend/", otp_resend),
    path("login/otp/generate/", login),
    path("login/otp/verify/", login_otp_verify),
    path("login/otp/resend/", login_otp_resend),
]
