from Crypto.Cipher import AES
import requests

SITE_FLAG = "https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag"
SITE_DECRYPT = "https://aes.cryptohack.org/ecbcbcwtf/decrypt"

cipher = requests.get(SITE_FLAG).json()["ciphertext"]

ENC_FLAG = cipher[32:]
IV = cipher[:32]

ENC_FLAG = bytes.fromhex(ENC_FLAG)
IV = bytes.fromhex(IV)


ecb_dec_flag = requests.get(f"{SITE_DECRYPT}/{ENC_FLAG.hex()}").json()["plaintext"]
ecb_dec_flag = bytes.fromhex(ecb_dec_flag)


dec_flag = ""
for i in range(len(IV)):
    dec_flag += chr(IV[i] ^ ecb_dec_flag[i])


for i in range(len(IV)):
    dec_flag += chr(ENC_FLAG[i] ^ ecb_dec_flag[len(IV) + i])

print(dec_flag)


