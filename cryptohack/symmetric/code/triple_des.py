from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
import os
import requests

SITE_ENC_FLAG = "https://aes.cryptohack.org/triple_des/encrypt_flag/{}"
SITE_ENC = "https://aes.cryptohack.org/triple_des/encrypt/{}/{}"

DES_WEAK_KEY_1 = "0000000000000000"
DES_WEAK_KEY_2 = "FEFEFEFEFEFEFEFE"

TRIPLE_DES_WEAK_KEY = DES_WEAK_KEY_1 + DES_WEAK_KEY_2 + DES_WEAK_KEY_1

enc_flag = requests.get(SITE_ENC_FLAG.format(TRIPLE_DES_WEAK_KEY)).json()["ciphertext"]

dec_flag = requests.get(SITE_ENC.format(TRIPLE_DES_WEAK_KEY, enc_flag)).json()["ciphertext"]

dec_flag = bytes.fromhex(dec_flag)

print(dec_flag)

