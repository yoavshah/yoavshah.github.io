from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import json
import string

SITE = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

# should be identical to the last block
START_PAD = 8
curr_found = b"}"
FLAG_SIZE = 25
for j in range(1, FLAG_SIZE):
    print(curr_found)
    
    for b in string.printable:
        bb = b.encode().hex()
        curr = bb
        
        number_of_paddings = (((((16 + START_PAD + j + FLAG_SIZE) // 16) + 1) * 16) - (16 + START_PAD + j + FLAG_SIZE)) % 16
        number_of_paddings = number_of_paddings
        if number_of_paddings == 0:
            number_of_paddings = 16

        pad_char = number_of_paddings.to_bytes(1, "little")
        
        FIRST_BLOCK = curr + curr_found[:15].hex() + pad_char.hex() * (16 - (len(curr_found[:15]) + 1))

        FILL_BLOCK = "00" * (j + START_PAD)

        # FIRST [Brute force first character]
        # SHIT
        # FIRST
        FULL_BLOCK = FIRST_BLOCK + FILL_BLOCK
        
        k = requests.get(SITE + FULL_BLOCK).json()

        ctext = k["ciphertext"]

        c_first_block = ctext[:32]
        c_second_block = ctext[32:64]
        c_third_block = ctext[64:64+32]
        c_fourth_block = ctext[64+32:64+32 + 32]

        if c_first_block == c_fourth_block:
            print("found char " + b)
            curr_found = b.encode() + curr_found
            break
    else:
        print("Failed to find for " + str(j))
        break 
