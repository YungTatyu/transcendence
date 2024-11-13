## 公開鍵と秘密鍵を生成
# 秘密鍵を生成
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048

# 公開鍵を生成
openssl rsa -pubout -in private.pem -out public.pem

## ユーザー作成

~$curl -X POST http://127.0.0.1:8000/api/users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
  }'

{"message":"User created successfully"}%

## JWTトークン取得

~$curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

response
{"access_token": "<JWT TOKEN>"}%

## 公開鍵の取得
curl -X GET http://127.0.0.1:8000/api/public-key/

## JWTで保護されたエンドポイントへのアクセス

curl -X GET http://127.0.0.1:8001/api/secure/ \
  -H "Authorization: Bearer <JWT TOKEN>"
