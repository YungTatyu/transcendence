"""
URL configuration for auth_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

from auth_app.views.health_check_view import HealthCheckView
from auth_app.views.otp_login_view import OTPLoginVerificationView, OTPLoginView
from auth_app.views.signup_views import OTPVerificationView, SignupView
from auth_app.views.token_refresh_view import TokenRefreshView
from auth_app.views.update_email_view import UpdateEmailView
from auth_app.views.update_password_view import UpdatePasswordView

urlpatterns = [
    path("auth/otp/signup", SignupView.as_view(), name="otp-signup"),
    path(
        "auth/otp/signup/verify",
        OTPVerificationView.as_view(),
        name="otp-signup-verify",
    ),
    path("auth/me/email", UpdateEmailView.as_view(), name="update_email"),
    path("auth/me/password", UpdatePasswordView.as_view(), name="update_password"),
    path("auth/otp/login", OTPLoginView.as_view(), name="otp-login"),
    path(
        "auth/otp/login/verify",
        OTPLoginVerificationView.as_view(),
        name="otp-login-verify",
    ),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("health", HealthCheckView.as_view(), name="health_check"),
    path("", include("django_prometheus.urls")),
]
