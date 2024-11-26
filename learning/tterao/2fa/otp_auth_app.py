#! /usr/bin/python3

import pyotp
import qrcode

# 秘密鍵を生成
secret = pyotp.random_base32()

# URIを生成
totp = pyotp.TOTP(secret)
provisioning_uri = totp.provisioning_uri(
    name="uenomiya.2013@gmail.com", issuer_name="2fa"
)

print(provisioning_uri)

# QRコードを生成
qr = qrcode.make(provisioning_uri)

# QRコードを保存または表示
qr.save("otp_qr.png")  # ファイルに保存
qr.show()  # 画面に表示

while True:
    totp = pyotp.TOTP(secret)
    otp = input("Enter your otp: ")
    print(totp.verify(otp))
