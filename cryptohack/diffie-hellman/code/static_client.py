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


def get_alice_params():
    r = remote('socket.cryptohack.org', 13373)

    alice_params = get_json(r.recvline())
    bob_params = get_json(r.recvline())
    flag_params = get_json(r.recvline())

    _ = r.recv(4096)
    _ = r.recv(4096)

    r.close()

    return alice_params, flag_params

    
def get_bob_secret(a, g, p):
    
    t = 2
    
    while True:
        try:
            r = remote('socket.cryptohack.org', 13373)
            print("Connected")
            
            alice_params = get_json(r.recvline(timeout=t))
            bob_params = get_json(r.recvline(timeout=t))
            flag_params = get_json(r.recvline(timeout=t))
            
            _ = r.recv(4096, timeout=t)
            if len("Bob connects to you, send him some parameters: ") != len(_):
                _ = r.recv(4096, timeout=t)
                
            my_A = pow(g, a, p)
            my_params = {"p": hex(p), "g": hex(g), "A": hex(my_A)}
            
            r.send(json.dumps(my_params).encode())
            new_bob_params = get_json(r.recvline(timeout=t))
            new_flag_params = get_json(r.recvline(timeout=t))

            r.close()

            return int(new_bob_params["B"], 16)
        
        except Exception as e:
            print(e)
            time.sleep(1)

# Get primes under limit
def sieve_of_eratosthenes(limit):
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, limit + 1, i):
                primes[j] = False

    return [i for i in range(2, limit + 1) if primes[i]]


alice_params, flag_params = get_alice_params()
alice_p = int(alice_params["p"], 16)

alice_p_bit_length = alice_p.bit_length()


prime_numbers = [x for x in sieve_of_eratosthenes(3000) if x >= 1800]
prime_numbers.reverse()

reminders = []
for i, current_prime in enumerate(prime_numbers):
    
    current_p = (1 << current_prime) - 1
    
    B = get_bob_secret(1, 2, current_p)

    l = int(math.log2(B))
    
    reminders.append((l, current_prime, True))
    
    print(f"[{i}]Found log2 = {l}")


print("Found all reminders")

candidate_b = chinese_remainder_theorem.chinese_reminder_faster(reminders)

print(f"Found candidate_b = {candidate_b}")

# use this candidate to bruteforce real b

# B = 2 ** b
B = get_bob_secret(1, 2, alice_p)

i = 1
while True:
    curr_candidate_b = (candidate_b * i) % alice_p

    if pow(2, curr_candidate_b, alice_p) == B:
        print("Found the real b: " + str(curr_candidate_b))
        break

b = curr_candidate_b

shared_secret = pow(int(alice_params["A"], 16), b, alice_p)

# decrypt flag
dec_flag = decrypt_flag(shared_secret, flag_params["iv"], flag_params["encrypted"])

print(dec_flag)




