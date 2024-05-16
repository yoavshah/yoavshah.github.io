from pwn import *
import json
import base64
import hashlib
from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes
import hashlib


# https://github.com/corkami/collisions/tree/master?tab=readme-ov-file#unicoll-md5
# https://github.com/cr-marcstevens/hashclash?tab=readme-ov-file#create-you-own-identical-prefix-collision
# https://github.com/cr-marcstevens/hashclash/blob/master/scripts/poc_no.sh


# Use the script above to create 2 messages,
# one of them with the specific prefix "CryptoHack Secure Safe" (set it to be "CryptoHack Secure Safe00" for padding)
# Because the unlock function xors are canceled, we just need 2 keys with the
# same hash and that one of them starts with the prefix and the other without it.

key1 = "43727970746f4861636b20536563757265205361666530300b855fcf9a6a4347557ac4ac39cd6fd4c875c3d3f18cb05c4bf3f46f083c91dd62040f704d72ebf9b32438b5b55454799a201c1b24563a6c836d6dde9b18e2890390d9b2a0e07705dafbbaf8cb19a00e2398f42fcbd8d8f22f3c3869c9147df148d94f9477002230"
key2 = "43727970746f4861636c20536563757265205361666530300b855fcf9a6a4347557ac4ac39cd6fd4c875c3d3f18cb05c4bf3f46f083c91dd62040f704d72ebf9b32438b5b55454799a1f1c1b24563a6c836d6dde9b18e2890390d9b2a0e07705dafbbaf8cb19a00e2398f42fcbd8d8f22f3c3869c9147df148d94f9477002230"

key1 = bytes.fromhex(key1)
key2 = bytes.fromhex(key2)

print("Key1[:20]")
print(key1[:20])

print("Key2[:20]")
print(key2[:20])

r = remote('socket.cryptohack.org', 13397, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)



_ = r.recvline()

json_send({"option": "insert_key", "key": key1.hex()})
_ = json_recv()

json_send({"option": "insert_key", "key": key2.hex()})
_ = json_recv()

json_send({"option": "unlock"})
msg = json_recv()["msg"]

print(msg)


r.close()



