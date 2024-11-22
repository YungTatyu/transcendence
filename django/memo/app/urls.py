from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
        path('', views.index, name='index'),
        path('<int:memo_id>', views.detail, name='detail'),
        path('new_memo',views.new_memo, name='new_memo'),
        path('delete_memo/<int:memo_id>', views.delete_memo, name='delete_memo'),
        path('edit_memo/<int:memo_id>', views.edit_memo, name='edit_memo'),

]
