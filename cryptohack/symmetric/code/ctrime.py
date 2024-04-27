from Crypto.Cipher import AES
from Crypto.Util import Counter
import zlib
import requests
import string

SITE = "https://aes.cryptohack.org/ctrime/encrypt/{}"

FLAG = b"crypto{"
USED_FLAG = FLAG

curr_plain = FLAG.hex()
lastlen = len(requests.get(SITE.format(curr_plain)).json()["ciphertext"])

print("Length of the compressed data " + str(lastlen))

lastc = ""

padding = b"\x00"

while lastc != "}":

    curr_plain = FLAG.hex()
    for c in string.printable.encode():
        
        curr_text = padding.hex() + USED_FLAG.hex() + c.to_bytes(1, "little").hex()

        l = len(requests.get(SITE.format(curr_text)).json()["ciphertext"])
        if l == lastlen:
            print("found char " + chr(c))
            lastc = chr(c)
            FLAG += c.to_bytes(1, "little")
            USED_FLAG += c.to_bytes(1, "little")
            print(FLAG)
            break
        
    else:
        print("Could not find it, removing first data from flag")

        USED_FLAG = USED_FLAG[1:]
        
        curr_text = USED_FLAG.hex()
        print(SITE.format(curr_text))

        lastlen = len(requests.get(SITE.format(curr_text)).json()["ciphertext"])
        print("Found new length " + str(lastlen))

