from Crypto.Cipher import AES
import os
from pyfinite import ffield
from Crypto.Util.number import long_to_bytes, bytes_to_long
import galois
import requests


SITE_ENC = "https://aes.cryptohack.org/forbidden_fruit/encrypt/{}"
SITE_DEC = "https://aes.cryptohack.org/forbidden_fruit/decrypt/{}/{}/{}/{}"

def encrypt(plaintext):
    
    return requests.get(SITE_ENC.format(plaintext.hex())).json()

def decrypt(nonce, ciphertext, tag, associated_data):

    get_params = SITE_DEC.format(nonce.hex(), ciphertext.hex(), tag.hex(), associated_data.hex())
    return requests.get(get_params).json()

def rev_bits(x):
    return int("{:0128b}".format(x)[::-1], 2)

irreducible_poly = (1 << 128) + (1 << 7) + (1 << 2) + (1 << 1) + (1 << 0)
GF = ffield.FField(128, gen=irreducible_poly)
F = galois.GF(2**128, irreducible_poly=irreducible_poly)

# Fields function
def FAdd(x, y):
    return rev_bits((F(rev_bits(x)) + F(rev_bits(y))).all())

def FMul(x, y):
    return rev_bits((F(rev_bits(x)) * F(rev_bits(y))).all())

def FInv(x):
    return rev_bits(GF.Inverse(rev_bits(x)))

def FPow(num, exp):
    total = 1 << 128
    while exp != 0:

        if exp % 2 == 0:
            num = FMul(num, num)
            
            exp = exp // 2
        
        else:
            total = FMul(total, num) 
            exp = exp - 1
            
    return total


plaintextA = b"a"*16
plaintextB = b"b"*16

Xa = encrypt(plaintextA)
tagA = bytes_to_long(bytes.fromhex(Xa["tag"]))
ca = bytes_to_long(bytes.fromhex(Xa["ciphertext"]))

Xb = encrypt(plaintextB)
tagB = bytes_to_long(bytes.fromhex(Xb["tag"]))
cb = bytes_to_long(bytes.fromhex(Xb["ciphertext"]))

# nonce is used multiple times
nonce = bytes.fromhex(Xa["nonce"])

# tagA = (((((aad * H) + CA1) * H) + len) * H) + X
# tagB = (((((aad * H) + CB1) * H) + len) * H) + X
# tagA + tagB = ((((aad * H) + CA1) * H) + len) * H)  + (((((aad * H) + CB1) * H) + len) * H)
# = (aad * H ** 3 + CA1 * H ** 2 + len * H) + (aad * H ** 3 + CB1 * H ** 2 + len * H)
# = CA1 * H ** 2 + CB1 * H ** 2 = (CA1 + CB1) * H ** 2
# => (tagA + tagB) = (CA1 + CB1) * H ** 2 
# => H ** 2 = (tagA + tagB) * Inv(CA1 + CB1)
# => H = sqrt((tagA + tagB) * Inv(CA1 + CB1))

print("Finding H")
tagsSum = FAdd(tagA, tagB)
cSum = FAdd(ca, cb)
invCSum = FInv(cSum)
hPowered = FMul(invCSum, tagsSum)

# SQRT https://crypto.stackexchange.com/a/17992
H = FPow(hPowered, 2**(GF.n - 1))
print("H: " + long_to_bytes(H).hex())

print("Finding E0")
aad = b'CryptoHack'
len_aad = len(aad)

ca = long_to_bytes(ca)
len_ciphertext = len(plaintextA)

# pad aad
aad = aad + (16 - len(aad))*b"\x00"
caPadded = ca + (16 - len(ca))*b"\x00"

block_length = long_to_bytes(((8 * len_aad) << 64) | (8 * len_ciphertext))

Ta = 0
Ta = FAdd(Ta, bytes_to_long(aad))
Ta = FMul(Ta, H)
Ta = FAdd(Ta, bytes_to_long(caPadded))
Ta = FMul(Ta, H)
Ta = FAdd(Ta, bytes_to_long(block_length))
Ta = FMul(Ta, H)
E0 = FAdd(Ta, tagA)

print("E0: " + long_to_bytes(E0).hex())


print("Getting the ciphertext of \"give me the flag\" without tag")
plaintextFlag = b"give me the flag"
encFlag = encrypt(plaintextFlag)
cFlag = bytes.fromhex(encFlag["ciphertext"])

# Use E0 and H to sign the new ciphertext
print("Using E0 and H to sign the new ciphertext")

header = b'CryptoHack'
aad = b'CryptoHack'

len_aad = len(aad)
len_ciphertext = len(cFlag)

# pad aad
aad = aad + (16 - len(aad))*b"\x00"
cFlagPad = cFlag + (16 - len(cFlag))*b"\x00"
block_length = long_to_bytes(((8 * len_aad) << 64) | (8 * len_ciphertext))

print("Starting signing")

Ta = 0
Ta = FAdd(Ta, bytes_to_long(aad))
Ta = FMul(Ta, H)
Ta = FAdd(Ta, bytes_to_long(cFlag))
Ta = FMul(Ta, H)
Ta = FAdd(Ta, bytes_to_long(block_length))
Ta = FMul(Ta, H)
tagFlag = FAdd(Ta, E0)

tagFlag = long_to_bytes(tagFlag)

print("Sending decryption parameters")
flagDec = decrypt(nonce, cFlag, tagFlag, header)

flag = bytes.fromhex(flagDec["plaintext"]).decode()
print("Flag: " + flag)

