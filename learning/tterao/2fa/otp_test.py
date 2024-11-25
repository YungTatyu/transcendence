#! /usr/bin/python3

import pyotp
import time
import datetime

secrets = {}
otps = {}
for i in range(5):
    key = pyotp.random_base32()
    secrets[i] = key
    print(key)
    tocp = pyotp.TOTP(key, interval=30)
    otp = tocp.now()
    print(otp)
    otps[i] = otp


for i, key in secrets.items():
    tocp = pyotp.TOTP(secrets[i])
    print(tocp.verify(otps[i]))
    time_remaining = tocp.interval - (
        datetime.datetime.now().timestamp() % tocp.interval
    )
    print("remaintime:", time_remaining)

time.sleep(30)
for i, key in secrets.items():
    tocp = pyotp.TOTP(secrets[i])
    print(tocp.verify(otps[i]))
    time_remaining = tocp.interval - (
        datetime.datetime.now().timestamp() % tocp.interval
    )
    print("remaintime:", time_remaining)

# OTP verified for current time
# totp.verify("492039")  # => True
# time.sleep(30)
# totp.verify("492039")  # => False
