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
{"access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzEzMzYyNDYsImlhdCI6MTczMTMzMjY0Nn0.A7OE5ddnd2AtS7SirakfNLX_m3eML-hc0BKm3Np4HjINlhdugTB0Q5YjjvkS2ca-FNeqxe9ABWYadoA51SzR7ADWGHqSXrfciPdK9x2xCDIXyfNFIDa248381oxN1ulJa-W74I1obbhx5rRth4PRe6iqKrptB232nqBgoBdRMQ2Ufo2Au6Zst-RRVpKf5_psanUQtdtShG9x2czRqbgsBhynXTnratEEKAnHsxQEvEHdvQis0PZzCAPyR7Xbr8rcpyWdQwebUIEvG8fwm6HMZkB2j0TyzDuyu5BpHEMmlQiWfqOD4151CdKWsW5qTFBGTstBqIwZp8eSGAo2JPfaNg"}%

## 公開鍵の取得
curl -X GET http://127.0.0.1:8000/api/public-key/
