from pwn import *
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import number
import hashlib
import collections
import os
from tqdm import tqdm

from helpers import chinese_remainder_theorem
from helpers import prime_factors

import time

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
    
def get_json(s):
    return json.loads(s[s.index(b"{"):])


r = remote('socket.cryptohack.org', 13380)

alice_params = get_json(r.recvline())
bob_params = get_json(r.recvline())
flag_params = get_json(r.recvline())

r.close()


# find inverse of g in p
g = int(alice_params["g"], 16)
p = int(alice_params["p"], 16)

g_inv = pow(g, p - 2, p)

B = int(bob_params["B"], 16)
b = (B * g_inv) % p

# calculate shared secret

shared_secret = (int(alice_params["A"], 16) * b) % p
dec_flag = decrypt_flag(shared_secret, flag_params["iv"], flag_params["encrypted"])
print(dec_flag)
