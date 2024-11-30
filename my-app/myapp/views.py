from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

# 一覧表示
def item_list(request):
    items = Item.objects.all()
    return render(request, 'myapp/item_list.html', {'items': items})

'''
# コードの説明
・ Item.objects.all() で、データベースからすべてのItemを取得します。
・ render関数でテンプレート'myapp/item_list.html'を呼び出し、取得したデータ（items）をテンプレートに渡して表示します。
'''


# 作成
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'myapp/item_form.html', {'form': form})

'''
# コードの説明
・ request.methodでリクエストがPOST（送信されたデータ）であるか確認します。
・ POSTの場合はフォームデータからItemFormを作成し、データが正しいか確認（form.is_valid()）した後、データを保存します。
・ 保存後は一覧ページにリダイレクトします。
・ POSTでなければ空のフォームを作成し、item_form.htmlテンプレートに表示します。
'''


# 更新
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'myapp/item_form.html', {'form': form})

'''
# コードの説明
・ get_object_or_404で、データベースからpk（プライマリキー）に該当するItemを取得します。
・ POSTリクエストの場合、フォームが送信され、データをitemに上書きする形でフォームを作成します。
・ データが正しければ保存し、一覧ページにリダイレクトします。
・ POSTでなければ既存のItemの内容を反映したフォームを作成し、テンプレートに表示します。
'''


# 削除
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})

'''
# コードの説明
・ get_object_or_404でデータベースからpkに該当するItemを取得します。
・ POSTリクエストの場合はitem.delete()でデータを削除し、一覧ページにリダイレクトします。
・ POSTでない場合、削除確認ページitem_confirm_delete.htmlを表示し、ユーザーが本当に削除を行うか確認します。
'''