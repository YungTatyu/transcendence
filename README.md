# マイクロサービスとJWT認証サンプル実装

このリポジトリは、マイクロサービスアーキテクチャを使用して構築され、JWT（JSON Web Token）認証を通じてセキュリティが強化されたサンプルサーバーです。以下にユーザーの作成、トークン取得、保護されたエンドポイントへのアクセス方法を示します。

## 構成

- ユーザー認証
- JWTトークンを使用した認証
- 公開鍵の取得
- JWTで保護されたエンドポイントへのアクセス

## 必要条件

- Docker（コンテナ環境で実行する場合）
- cURL（APIリクエストを送信するため）

## 実行手順

### 1. ユーザー作成

まず、ユーザーを作成するためのAPIエンドポイントにリクエストを送信します。

```bash
curl -X POST http://127.0.0.1:8000/api/users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
  }'

{
  "message": "User created successfully"
}
```

### 2. JWTトークン取得
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

{
  "access_token": "<JWT TOKEN>"
}
```

### 3. JWTで保護されたエンドポイントへのアクセス
```bash
curl -X GET http://127.0.0.1:8001/api/secure/ \
  -H "Authorization: Bearer <JWT TOKEN>"

{"message": "Authenticated", "user_id": 1}
```

### DBコンテナ内のデータベースへの接続
```
docker exec -it auth_db psql -U auth_user -d auth_db
```
