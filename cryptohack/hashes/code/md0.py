from pwn import *
import json
import base64
import hashlib
from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes
import hashlib
from Crypto.Cipher import AES


def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


r = remote('socket.cryptohack.org', 13388, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)



_ = r.recvline()

first_message = b"\x00" * 15
first_message_padded = first_message + b"\x01"
json_send({"option": "sign", "message": first_message.hex()})
sig_first = bytes.fromhex(json_recv()["signature"])


blk = b"admin=True"
blk += b"\x00" * (15 - len(blk))
blk_padded = blk + b"\x01"

second_message = first_message_padded + blk

new_signature = bxor(AES.new(blk_padded, AES.MODE_ECB).encrypt(sig_first), sig_first)

json_send({"option": "get_flag",
           "message": second_message.hex(),
           "signature": new_signature.hex()})

flag = json_recv()


r.close()



