from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

# UserCreationForm とUSerCanggeFormを継承してemailフィールドを追加


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

    email = forms.EmailField()

class CustomUSerChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    
    email = forms.EmailField()