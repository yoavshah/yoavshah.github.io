from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
import requests

SITE_ENCRYPT = "https://aes.cryptohack.org/lazy_cbc/encrypt/{}"
SITE_DECRYPT = "https://aes.cryptohack.org/lazy_cbc/receive/{}"
SITE_GET_FLAG = "https://aes.cryptohack.org/lazy_cbc/get_flag/{}"

zero_block = "00" * 16 # 16 bytes

to_encrypt = zero_block
enc_key = requests.get(SITE_ENCRYPT.format(to_encrypt)).json()["ciphertext"]

to_decrypt = zero_block + enc_key
error_dec = requests.get(SITE_DECRYPT.format(to_decrypt)).json()["error"]

dec = error_dec[len("Invalid plaintext: "):]

first_block_decrypted = dec[:32]
second_block_decrypted = dec[32:64]

key = second_block_decrypted

flag = requests.get(SITE_GET_FLAG.format(key)).json()["plaintext"]

flag = bytes.fromhex(flag)

print(flag)
