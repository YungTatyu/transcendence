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

  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzE0MDg0MDgsImlhdCI6MTczMTQwNDgwOH0.IeWdG3TTmbxFjP1DNnSkN2vidkIxO04WDDE8eu2dOciQwV5pQSZzzCzQyACXC-yRa6ZebK7CW-r983iElHwe1iTO45bQnjcKs5C2SRsw9gF5O9Txk-sZMcPyD8cHzGJFbizaYbCU_RinzJkZwYzjU_w5X2rdVxNJbtSBmGiwTCl0lnrn6olHWCYn-G3NNoUWEkEgT11FbQeT_PSGUjdZxeKNVQJR9WgwETvx1-vgxka4xduROCMsjgmvGPyfigMIyA9DFZZZpcWkNEeMASBezSvYQ-BfdXn-3jkNC7ekVVPYaSFXTUuy833x5BowOFlr6vF3ViUhpy7UyYi7z2-nHA
