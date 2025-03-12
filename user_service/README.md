
コンテナを立ち上げたあと、以下のコマンドでアバターのアップロードが可能。(avatar_pathは各自変更してください)

```sh
 curl -X PUT -H "Content-Type: multipart/form-data" -F "avatar_path=@/home/yuna/Downloads/image.png" http://localhost:9000/users/me/avatar
```

レスポンス
```sh 
{"avatarPath":"/uploads/avatars/12345.png"}% 
```