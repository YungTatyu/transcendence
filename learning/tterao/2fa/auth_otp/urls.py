from django.urls import path
from .views import otp_generate, otp_verify, otp_resend


urlpatterns = [
    # path("signup/", signup),
    path("otp/generate/", otp_generate),
    path("otp/verify/", otp_verify),
    path("otp/resend/", otp_resend),
]
