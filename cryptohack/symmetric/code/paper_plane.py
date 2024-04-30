from Crypto.Util.Padding import pad, unpad
import requests

SITE_ENC_FLAG = "https://aes.cryptohack.org/paper_plane/encrypt_flag"
SITE_SEND_MSG = "https://aes.cryptohack.org/paper_plane/send_msg/{}/{}/{}"

def _is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def send_msg(cipher, m0, c0):
    r = requests.get(SITE_SEND_MSG.format(cipher.hex(), m0.hex(), c0.hex())).json()

    if "error" in r.keys():
        return False
    elif "msg" in r.keys():
        return True

enc = requests.get(SITE_ENC_FLAG).json()

enc_flag = bytes.fromhex(enc["ciphertext"])
m0_flag = bytes.fromhex(enc["m0"])
c0_flag = bytes.fromhex(enc["c0"])
enc_block0_flag = enc_flag[:16]
enc_block1_flag = enc_flag[16:32]
    

KNOWN_FIRST_BLOCK = b""
for i in range(len(KNOWN_FIRST_BLOCK) + 1, 17):

    number_of_unchanged_chars = 16 - i
    v = []
    
    # Bruteforce for loop
    for j in range(256):
        
        # Calculate c0
        curr_c0 = c0_flag[:number_of_unchanged_chars]

        curr_c0 += j.to_bytes(1, "little")

        for k in range(len(KNOWN_FIRST_BLOCK)):
            b = KNOWN_FIRST_BLOCK[k] ^ c0_flag[k + number_of_unchanged_chars + 1] ^ i
            
            curr_c0 += b.to_bytes(1, "little")

        
        s = send_msg(enc_block0_flag, m0_flag, curr_c0)
        v.append(s)
        
    indices = [ind for ind, x in enumerate(v) if x and ind != c0_flag[number_of_unchanged_chars]]
    m2_other_byte = indices[0] ^ i ^ c0_flag[number_of_unchanged_chars]

    KNOWN_FIRST_BLOCK = chr(m2_other_byte).encode() + KNOWN_FIRST_BLOCK
    print(KNOWN_FIRST_BLOCK)


KNOWN_SECOND_BLOCK = b""
for i in range(len(KNOWN_SECOND_BLOCK) + 1, 17):

    number_of_unchanged_chars = 16 - i
    v = []
    # Bruteforce for loop
    for j in range(256):
        
        # Calculate c1
        curr_enc_flag = enc_block0_flag[:number_of_unchanged_chars]

        curr_enc_flag += j.to_bytes(1, "little") # Bruteforce char

        for k in range(len(KNOWN_SECOND_BLOCK)):
            b = KNOWN_SECOND_BLOCK[k] ^ enc_block0_flag[k + number_of_unchanged_chars + 1] ^ i
            curr_enc_flag += b.to_bytes(1, "little")
            
        curr_enc_flag += enc_block1_flag

        # Calculate m0
        curr_m0 = m0_flag[:number_of_unchanged_chars]

        # Calculate the current bruteforce fixing byte
        curr_m0 += (j ^ enc_block0_flag[number_of_unchanged_chars] ^ m0_flag[number_of_unchanged_chars]).to_bytes(1, "little")

        for k in range(len(KNOWN_SECOND_BLOCK)):
            # i ^ enc_block0_flag[-1] ^ m0_flag[-1]).to_bytes(1, "little")
            b = enc_block0_flag[k + number_of_unchanged_chars + 1] ^ curr_enc_flag[k + number_of_unchanged_chars + 1] ^ m0_flag[k + number_of_unchanged_chars + 1]
            curr_m0 += b.to_bytes(1, "little")

        #print(curr_m0)
        s = send_msg(curr_enc_flag, curr_m0, c0_flag)
        v.append(s)
        
    indices = [ind for ind, x in enumerate(v) if x and ind != enc_block0_flag[number_of_unchanged_chars]]
    if len(indices) == 0:
        indices = [enc_block0_flag[number_of_unchanged_chars]]
        
    m2_other_byte = indices[0] ^ i ^ enc_block0_flag[number_of_unchanged_chars]

    KNOWN_SECOND_BLOCK = chr(m2_other_byte).encode() + KNOWN_SECOND_BLOCK
    print(KNOWN_SECOND_BLOCK)
    
print(KNOWN_FIRST_BLOCK + KNOWN_SECOND_BLOCK)



