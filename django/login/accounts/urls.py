from django.urls import path
from . import views

#ユーザー登録用のURLパターン

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]