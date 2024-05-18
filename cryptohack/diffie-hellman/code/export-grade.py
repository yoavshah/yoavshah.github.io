from pwn import *
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import collections
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


def prime_factors(n):
    
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n = n // 2


    i = 3
    n_sqrt = math.sqrt(n)
    while i <= n_sqrt:
        if n % i != 0:
            i += 2
            
        else:
            n //= i
            factors.append(i)
            print(factors)
            
    if n > 1:
        factors.append(n)
        
    return factors

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


# Pohlig-Hellman's Algorithm
#p_factors = prime_factors(p - 1)
p_factors = [2, 3, 293, 5417, 420233272499]
print(p_factors)

factors_counter = collections.Counter(p_factors)

factors_counter_keys = list(factors_counter.keys())

pows_mods = []
for q in factors_counter_keys:
    print("Calculating on " + str(q))
    e = factors_counter[q]

    # h = g
    # g = A

    g_pow_div = pow(A, (p-1) // (q ** e), p)
    h_pow_div = pow(g, (p-1) // (q ** e), p)

    # g_pow_div ** x = h_pow_div
    # Brute force x

    next_pow = 1
    exp = 0
    while True:
        if next_pow == h_pow_div:
            break

        next_pow = (next_pow * g_pow_div) % p
        exp += 1

    # this is mode q1 ** e1
    pows_mods.append((next_pow, q ** e))
    






# Try to find the secret a or the secret b
##x = g
##i = 1
##
##is_a = False
##while True:
##    if x == A:
##        is_a = True 
##        break
##
##    if x == B:
##        is_a = False
##        break
##
##    x = (x * g) % p
##    i += 1
##
##    if i % 100000000 == 0:
##        print(str(i) + " - " + str(x))
##
##
##if is_a:
##    shared_secret = pow(B, i, p)
##else:
##    shared_secret = pow(A, i, p)
##
##dec_flag = decrypt_flag(shared_secret, enc_flag["iv"], enc_flag["encrypted_flag"])
##
##print(dec_flag)

#r.close()



