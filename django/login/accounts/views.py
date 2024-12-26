from django.shortcuts import render

#ユーザー登録のsignupビューを定義

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm 
from django.contrib.auth import login

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    #処理が成功した場合のリダイレクト先を指定
    cuccess_url = reverse_lazy('chat:caht_room')
    template_name = 'registration/signup.html'

    def form_vaild(self, form):
        """
        ユーザー登録直後の自動的にログオンさせる
        self.objectにsave()されたユーザーオブジェクトが格納されている
        """
        valid = super().form_vaild(form)
        login(self.request, self.object)
        return valid
    
