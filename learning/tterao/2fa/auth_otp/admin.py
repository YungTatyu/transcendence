from django.contrib import admin
from .models import User, UserTwoFactorSetup, UserTwoFactorVerification

admin.register(User, UserTwoFactorSetup, UserTwoFactorVerification)(admin.ModelAdmin)
