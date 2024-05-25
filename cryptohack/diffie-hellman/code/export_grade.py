from pwn import *
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import collections

#from helpers import pohlig_hellman
from helpers import pohlig_hellman_and_bsgs


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


r = remote('socket.cryptohack.org', 13379, level = 'debug')

_ = r.recvline()
_ = r.recv()

r.sendline(json.dumps({"supported": ["DH64"]}).encode())

_ = r.recvline()
_ = r.recv()

r.sendline(json.dumps({"chosen": "DH64"}).encode())

alice_dh_params = get_json(r.recvline())
bob_dh_params = get_json(r.recvline())
enc_flag = get_json(r.recvline())

p = int(alice_dh_params["p"], 16)
g = int(alice_dh_params["g"], 16)
A = int(alice_dh_params["A"], 16)
B = int(bob_dh_params["B"], 16)

r.close()


# g ** a = A mod p => find a
found_a = pohlig_hellman_and_bsgs.discrete_log(g, A, p)

# calculate shared secret
# B ** found_a mod p 
shared_secret = pow(B, found_a, p)

# decrypt flag
dec_flag = decrypt_flag(shared_secret, enc_flag["iv"], enc_flag["encrypted_flag"])

print(dec_flag)




