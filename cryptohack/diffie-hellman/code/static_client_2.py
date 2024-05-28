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
from Crypto.Util.number import isPrime

from helpers import chinese_remainder_theorem
from helpers import prime_factors
from helpers import baby_step_giant_step as bsgs
from helpers import pohlig_hellman_and_bsgs


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


def get_bob_params(g, p, A):
    r = remote('socket.cryptohack.org', 13378, level="debug")

    alice_params = get_json(r.recvline())
    bob_params = get_json(r.recvline())
    flag_params = get_json(r.recvline())

    my_params = {"p": hex(p), "g": hex(g), "A": hex(A)}
    
    r.send(json.dumps(my_params).encode())
    
    bob_params_2 = get_json(r.recvline())
    flag_params_2 = get_json(r.recvline())

    r.close()


    return int(bob_params_2["B"], 16)
    

def get_basic_params():
    r = remote('socket.cryptohack.org', 13378)

    alice_params = get_json(r.recvline())
    bob_params = get_json(r.recvline())
    flag_params = get_json(r.recvline())
    
    r.close()

    return alice_params, bob_params, flag_params



def get_prime_partial_factors(n, upper_bound):

    partial_factors = []
    for i in range(2, upper_bound):

        if n == 1:
            break
        
        while n % i == 0:
            partial_factors.append(i)
            n = n // i

    return partial_factors
        

def generate_prime_smooth(l):
    mul = 1
    i = 1
    while 1:
        mul *= i
        if (mul + 1).bit_length() >= l and isPrime(mul + 1):
            return mul + 1, i

        i += 1
        while not isPrime(i):
            i += 1


print("Getting basic parameters")

alice_params, bob_params, flag_params = get_basic_params()
my_a = int(alice_params["A"], 16)


prime_number, index = generate_prime_smooth(1700)
print(f"Generated prime number {prime_number}")

my_A = pow(2, my_a, prime_number)
current_B = get_bob_params(2, prime_number, 0x123456789123456789123456789)


b = pohlig_hellman_and_bsgs.discrete_log(2, current_B, prime_number)
print(f"Found b {b}")

shared_secret = pow(int(alice_params["A"], 16), b, int(alice_params["p"], 16))
                    
dec_flag = decrypt_flag(shared_secret, flag_params["iv"], flag_params["encrypted"])
print(dec_flag)






