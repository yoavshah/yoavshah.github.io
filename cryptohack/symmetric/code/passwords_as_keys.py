from Crypto.Cipher import AES
import hashlib
import random
import requests

WORDLIST = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
words = [w.strip() for w in requests.get(WORDLIST).text.split("\n")]

FLAG = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
    
ciphertext = bytes.fromhex(FLAG)
for w in words:
    
    key = hashlib.md5(w.encode()).digest()

    cipher = AES.new(key, AES.MODE_ECB)
    
    
    try:
        dec = cipher.decrypt(ciphertext).decode()
        print(dec)
        break
    except ValueError as e:
        pass




