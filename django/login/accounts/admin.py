from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUSerChangeForm
from .models import CustomUser
from django.utils.translation import gettext, gettext_lazy as _

#UserAdmin:ユーザーモデルをadminサイトに登録する

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUSerChangeForm
    model = CustomUser
    list_display=('pk', 'username', 'email')
    #fieldsetsをオーバライドしてthumbnailを加えることで変更画面に項目として表示されるようになる。
    fieldsets = (
        (None, {'fields': ('username', 'password', 'thumbnail')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    #add_fieldsetsのfieldsにthumbnailを加えると新規登録時の項目に追加される。
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','thumbnail'),
        }),
    )
admin.site.register(CustomUser, CustomUserAdmin)

