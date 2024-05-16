from pwn import *
import json
import base64
import hashlib
from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes
import hashlib



# https://en.wikipedia.org/wiki/Length_extension_attack
# https://github.com/corkami/collisions?tab=readme-ov-file#fastcoll-md5
# https://marc-stevens.nl/research/md5-1block-collision/


# Two known small collisions - can be computed
collision1 = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2"
collision2 = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2"


# Extend them with the same data so the hash will be
# the same but they will be 2 different numbers.
# Stop whenever one is prime and the other one is not prime.


print("Collision1: " + collision1)
print("Collision2: " + collision2)


print("Has the same hash")
print("md5(collision1): ", hashlib.md5(bytes.fromhex(collision1)).hexdigest())
print("md5(collision2): ", hashlib.md5(bytes.fromhex(collision2)).hexdigest())

extension_val = 0
while True:
    extension = long_to_bytes(extension_val)
    
    collision1_extended = bytes_to_long(bytes.fromhex(collision1) + extension)
    collision2_extended = bytes_to_long(bytes.fromhex(collision2) + extension)
    
    if isPrime(collision1_extended) and not isPrime(collision2_extended):
        break
    
    extension_val += 1

print("collision1_extended: ", collision1_extended)
print("collision2_extended: ", collision2_extended)

print("md5(collision1_extended) : ", hashlib.md5(long_to_bytes(collision1_extended)).hexdigest())
print("md5(collision2_extended) : ", hashlib.md5(long_to_bytes(collision2_extended)).hexdigest())


print("Finding appropriate gcd")

i = 1
mul = 1
temp_collision2_extended = collision2_extended
while True:
    if temp_collision2_extended % i == 0:
        mul *= i
        
        temp_collision2_extended = temp_collision2_extended // i
        
        if mul >= 40:
            break
        
    i += 1

r = remote('socket.cryptohack.org', 13392, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


math.gcd(collision2_extended, 5)

_ = r.recvline()


json_send({"option": "sign", "prime": collision1_extended})
signature = json_recv()["signature"]


json_send({"option": "check",
           "signature": signature,
           "prime": collision2_extended,
           "a": mul})

msg = json_recv()["msg"]

r.close()



