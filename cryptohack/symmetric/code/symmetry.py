import requests

SITE_ENC_FLAG = "https://aes.cryptohack.org/symmetry/encrypt_flag"
SITE_ENC = "https://aes.cryptohack.org/symmetry/encrypt/{}/{}"

enc = requests.get(SITE_ENC_FLAG).json()["ciphertext"]

iv = enc[:32]
enc_flag = enc[32:]

dec = requests.get(SITE_ENC.format(enc_flag, iv)).json()["ciphertext"]

dec = bytes.fromhex(dec)

print(dec)

