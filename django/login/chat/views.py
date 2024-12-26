from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.models import CustomUser
from django.views import View

#TOP画面を表示させるため
class Home(TemplateView):
    template_name = 'home.html'

#chatルーム画面に遷移する
class ChatRoom(TemplateView):
    template_name = 'chat/chat_box.html'


#友達リスト情報を取得
def getFriendsList(username):
    """
    指定したユーザーの友達リストを取得
    :param:ユーザー名
    :return:ユーザー名の友達リスト
    """
    try:
        #CustomUserクラスから該当ユーザ情報を取得しuser変数に格納
        user = CustomUser.objects.get(username=username)
        #逆参照でFriendsテーブルのデータを取得しfrineds変数にリスト型に変換して格納し、frinedsを戻り値として返す
        frineds = list(user.usera_friends.all())
    except:
        return []
    
#ユーザー情報を検索する
class SearchUser(View):

    #getメゾットを定義
    def get(self, request, *args, **kwargs):
        #検索画面から検索処理を実行したとき
        if 'search' in self.request.GET:
            query = request.GET.get("search")
            #全ユーザー情報を取得してリスト化
            users = list(CustomUser.objects.all())
            user_list = []
            for user in users:
                #検索文字列を含むユーザ情報を取得(自分は除外)
                if query in user.username and user.username != request.user.username:
                    user_list.append(user)
        else:
            #全ユーザ一覧を取得
            user_list = list(CustomUser.objects.all())  
            for user in user_list:
                if user.username == request.user.username:
                    #自分のユーザだけ除外
                    user_list.remove(user)  
                    break

        #自分のフレンド一覧を取得
        friends = getFriendsList(request.user.username)  
        return render(request, "chat/search.html", {'users': user_list, 'friends': friends})
    
def addFriend(request, username):
    """
    引数で受け取ったユーザ名(username)を Friendsテーブルに友達として登録する。
    """
    #現在ログオンしているユーザー名を取得
    login_user = request.user.username
    #友達追加するユーザー名のレコードを取得
    friend = CustomUser.objects.get(username=username)
    #ログオンユーザーのレコードを取得
    current_user = CustomUser.objects.get(username=login_user)
    #friendsクラスのレコードをすべて取得(ログオンユーザーのすべての友達情報が格納される)
    friend_lists = current_user.user_friends.all()
    #対象のユーザーが友達として登録済みかチェック　既に友達登録済みの場合flag=1にセット
    flag = 0
    for friend_list in friend_lists:
        if friend_list.friend.pk == friend.pk:
            flag = 1
            break
    #フレンド未登録の場合
    if flag == 0:
        #お互いにフレンド登録を行う。
        #ログオンユーザ視点でフレンドを登録
        current_user.user_friends.create(friend=friend)
        #フレンド視点でログオンユーザをフレンドに登録
        friend.user_friends.create(friend=current_user)
    #SerchUserクラスビューのget目ゾッドが実行　search.htmlにレンダリング
    return redirect("chat:search_user")