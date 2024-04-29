import requests
import random
from collections import Counter
import string
from Crypto.Cipher import ARC4

ascii_chars = [ord(x) for x in string.printable]

def send_req(cipher, nonce):

    try:
        SITE = "https://aes.cryptohack.org/oh_snap/send_cmd"
        current_site =  f"{SITE}/{cipher}/{nonce}"

        return requests.get(current_site).json()["error"].split("Unknown command: ")[1]

    except Exception as e:
        print(e)
        return None

flag_size = 34
flag_location = 256 - flag_size

known_flag = ""

def init_state():
    state = []
    for i in range(256):
        state.append(i)

    return state


def key_routine(state, key, l=256):
    index2 = 0
    for i in range(l):
        
        index2 = (index2 + key[i % len(key)] + state[i]) % 256
        
        t = state[i]
        state[i] = state[index2]
        state[index2] = t

    return index2

def next_key_routine(state, key, i, index2):
    index2 = (index2 + key[i % len(key)] + state[i]) % 256
    t = state[i]
    state[i] = state[index2]
    state[index2] = t

    return index2

def enc(state, cipher):
    x = 1
    y = state[x]

    t = state[x]
    state[x] = state[y]
    state[y] = t
    
    xorIndex = (state[x] + state[y]) % 256
    return cipher ^ state[xorIndex]


change_amount = 10
tests_amount = 100
for i in range(len(known_flag), flag_size):

    current_try = Counter()
    current_printable = Counter()
    curr_flag_pos = flag_location + i
    
    for t in range(tests_amount):
        
        key = curr_flag_pos.to_bytes(1, "little") # Get position to the first
        key += b"\xff" # Get 0 to the second

        s = init_state()
        
        index2 = 0
        index2 = next_key_routine(s, key, 0, index2)
        index2 = next_key_routine(s, key, 1, index2)

        # to make next index2 to be 2
        key += ((256 + 2) - (index2 + 2)).to_bytes(1, "little")
        index2 = next_key_routine(s, key, 2, index2)
        
        for j in range(3, flag_location - change_amount):
            key += ((256 + j) - (index2 + j)).to_bytes(1, "little")
            index2 = next_key_routine(s, key, j, index2)

        for j in range(flag_location - change_amount, flag_location):
            
            # generate random current key that will not change index 0 or 1
            key += random.randint(0, 255).to_bytes(1, "little")
            index2 = next_key_routine(s, key, j, index2)

      # This is the current weak key
        for j in range(flag_location, curr_flag_pos):
            
            key += known_flag.encode()[j - flag_location].to_bytes(1, "little")
            index2 = next_key_routine(s, key, j, index2)

            
        last_index2 = index2
        last_state = s.copy()

        ok_state = s.copy()
        other_val_cipher = int(send_req("00", key[:flag_location].hex()), 16)

        # Find where the value position was before starting with the unknown keys, that might be the index2 of it
        other_index2 = last_state.index(other_val_cipher)
                               
        suspected_key = ((other_index2 - last_index2  - last_state[curr_flag_pos]) + (256 * 5)) % 256

        if suspected_key in ascii_chars:  
            current_printable.update([suspected_key])
                

    c = chr(current_printable.most_common()[0][0])
    known_flag += c
    print(known_flag)
    

    
        
    


