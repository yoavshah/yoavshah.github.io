from Crypto.Cipher import AES
import os
import requests

SITE = "https://aes.cryptohack.org/bean_counter/encrypt"

enc_png = requests.get(SITE).json()["encrypted"]

enc_png = bytes.fromhex(enc_png)

first_block = enc_png[:16]

PNG_HEADER = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
CHUNK_HEADER = [0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52]

headers = PNG_HEADER + CHUNK_HEADER
key = [a^b for a, b in zip(first_block, headers)]


block_size = 16
current_block_index = 0
current_block = enc_png[block_size*current_block_index:block_size*(current_block_index+1)]
dec_png = b""

while current_block:
    dec_png += b"".join([t.to_bytes(1, "little") for t in [a^b for a, b in zip(key, current_block)]])
    current_block_index += 1
    current_block = enc_png[block_size*current_block_index:block_size*(current_block_index+1)]


f = open("bean_flag.png", "wb")
f.write(dec_png)
f.close()
