from django.urls import path
from .views import otp_generate, otp_verify, otp_regenerate


urlpatterns = [
    # path("signup/", signup),
    path("otp/generate/", otp_generate),
    path("otp/verify/", otp_verify),
    path("otp/regenerate/", otp_regenerate),
]
