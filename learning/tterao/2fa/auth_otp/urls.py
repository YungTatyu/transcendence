from django.urls import path
from .views import otp_generate, otp_verify


urlpatterns = [
    # path("signup/", signup),
    path("otp/generate/", otp_generate),
    path("otp/verify/", otp_verify),
]
