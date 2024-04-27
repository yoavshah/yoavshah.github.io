from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
import requests

SITE_GET_COOKIE = "https://aes.cryptohack.org/flipping_cookie/get_cookie"
SITE_CHECK_ADMIN = "https://aes.cryptohack.org/flipping_cookie/check_admin/{}/{}"

cookie = requests.get(SITE_GET_COOKIE).json()["cookie"]

iv = bytes.fromhex(cookie[:32])
enc = bytes.fromhex(cookie[32:])

needed = f"admin=True;"
exists = f"admin=False"

new_iv = b""

for i, _ in enumerate(needed):
    new_iv += (ord(needed[i]) ^ ord(exists[i]) ^ iv[i]).to_bytes(1, "little")

new_iv += iv[len(new_iv):]

print("COOKIE" + enc.hex())
print("IV: " + new_iv.hex())


flag = requests.get(SITE_CHECK_ADMIN.format(enc.hex(), new_iv.hex())).json()["flag"]

print(flag)


