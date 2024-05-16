from pwn import *
import json
import base64
import hashlib
from itertools import cycle
import string
import math


rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
             5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
             6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

init_MDBuffer = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

def leftRotate(x, amount):
    x &= 0xFFFFFFFF
    return (x << amount | x >> (32-amount)) & 0xFFFFFFFF

def get_pad_suffix(msg):
    d = len(msg) % 64
    msg_len_in_bits = (8*len(msg)) & 0xffffffffffffffff
    msg += b"\x80"
    while len(msg)%64 != 56:
        msg += b"\x00"

    
    msg += msg_len_in_bits.to_bytes(8, byteorder='little')
    return msg[-64 + d:]

    
def pad(msg):
    msg_len_in_bits = (8*len(msg)) & 0xffffffffffffffff
    msg.append(0x80)
    while len(msg)%64 != 56:
        msg.append(0)
        
    msg += msg_len_in_bits.to_bytes(8, byteorder='little')
    return msg

def pad_with_len(msg, msg_len):
    msg_len_in_bits = (8*msg_len) & 0xffffffffffffffff
    msg.append(0x80)
    while len(msg)%64 != 56:
        msg.append(0)

    msg += msg_len_in_bits.to_bytes(8, byteorder='little')
    return msg

def vector_to_hash(init_vector):
    return sum(buffer_content<<(32*i) for i, buffer_content in enumerate(init_vector))

def number_to_vector(number):
    return list(struct.unpack("<IIII", number.to_bytes(16, "little")))

def MD_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def hex_to_MD(h):
    return int.from_bytes(bytes.fromhex(h), "little")


def process_message_with_state(state, msg):
    init_temp = state #init_MDBuffer[:]

    for offset in range(0, len(msg), 64):
        A, B, C, D = init_temp 
        block = msg[offset : offset+64]
        for i in range(64):
            if i < 16:
                # Round 1
                func = lambda b, c, d: (b & c) | (~b & d)
                
                index_func = lambda i: i

            elif i >= 16 and i < 32:
                # Round 2
                func = lambda b, c, d: (d & b) | (~d & c)
                
                index_func = lambda i: (5*i + 1)%16

            elif i >= 32 and i < 48:
                # Round 3
                func = lambda b, c, d: b ^ c ^ d
                
                index_func = lambda i: (3*i + 5)%16
            
            elif i >= 48 and i < 64:
                # Round 4
                func = lambda b, c, d: c ^ (b | ~d)
                index_func = lambda i: (7*i)%16

            F = func(B, C, D) 
            G = index_func(i)

            to_rotate = A + F + constants[i] + int.from_bytes(block[4*G : 4*G + 4], byteorder='little')
            newB = (B + leftRotate(to_rotate, rotate_by[i])) & 0xFFFFFFFF
                
            A, B, C, D = D, newB, B, C

        for i, val in enumerate([A, B, C, D]):
            init_temp[i] += val
            init_temp[i] &= 0xFFFFFFFF

    return vector_to_hash(init_temp)

def process_message(msg):
    return process_message_with_state(init_MDBuffer[:], msg)


def md5(msg):
    msg = bytearray(msg) # create a copy of the original message in form of a sequence of integers [0, 256)
    msg = pad(msg)
    processed_msg = process_message(msg)
    # processed_msg contains the integer value of the hash
    message_hash = MD_to_hex(processed_msg)
   
    return msg, message_hash

# added function to md5 from a given state
def md5_with_state(state, msg, calculated_len):
    msg = bytearray(msg) # create a copy of the original message in form of a sequence of integers [0, 256)

    msg_len = calculated_len + len(msg)
    msg = pad_with_len(msg, msg_len)

    num_state = hex_to_MD(state)
    vector_state = number_to_vector(num_state)
    
    processed_msg = process_message_with_state(vector_state, msg)
    # processed_msg contains the integer value of the hash

    message_hash = MD_to_hex(processed_msg)
    
    return message_hash



# Start of the challenge


FLAG = "crypto{" + '_'*38 + "}"
FLAG = FLAG.encode()
FLAG_LENGTH = len(FLAG)

def json_recv(r):
    line = r.recvline()
    return json.loads(line.decode())

def json_send(r, hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def generate_block(data, block_size, block_index):

    cyc = cycle(data)
    for i in range(block_index + 1):
        res = b""
        for j in range(block_size):
            res += cyc.__next__().to_bytes(1, "little")
            
    return res

        

### Used at the start of the program to gain the flag length
##r = remote('socket.cryptohack.org', 13407, level = 'debug')
##_ = r.recvline()
##flag_size = 0
##while True:
##    json_send(r, {"option": "message", "data": (b"\x00"*flag_size).hex()})
##
##    res = json_recv(r)
##    if "error" in res and res["error"] == "Bad input":
##        pass
##    else:
##        break
##
##    flag_size += 1
##r.close()


print(generate_block(FLAG, 64, 2))


# Use the second block to find the last character of it (the first character in the flag)
# crypto{....} ....
# .....
# .............}crypto{A
# also ----------- 0x80 L

# First find the last byte in the second block
block_number = 2
data = b"\x00" * 64 * block_number
data += b"\x00" * (64 - 9)

known_suffix = get_pad_suffix(data)


r = remote('socket.cryptohack.org', 13407)#, level = 'debug')
_ = r.recvline()

json_send(r, {"option": "message", "data": data.hex()})
res_state = json_recv(r)["hash"]


pad_data = data + xor(known_suffix[:8], b"}crypto{") # It should produce known suffix

curr_valid_hash = md5_with_state(res_state, b"", (block_number + 1) * 64)

for c in range(256):
    curr_bruteforce_data = pad_data + c.to_bytes(1, "little")
    
    json_send(r, {"option": "message", "data": curr_bruteforce_data.hex()})
    curr_hash = json_recv(r)["hash"]

    if curr_hash == curr_valid_hash:
        break

r.close()
found_char = (known_suffix[8] ^ c).to_bytes(1, "little")


# Find the other bytes in iterable way
r = remote('socket.cryptohack.org', 13407)
_ = r.recvline()

s = b"}crypto{" + found_char

print(s)
for i in range(1, 38):
    data = b"\x00" * 64 * block_number
    data += b"\x00" * (64 - 9 - i)

    known_suffix = get_pad_suffix(data)

    json_send(r, {"option": "message", "data": data.hex()})
    res_state = json_recv(r)["hash"]

    pad_data = data

    curr_valid_hash = md5_with_state(res_state, b"", (block_number + 1) * 64)
    
    for c in range(256):
        curr_bruteforce_data = pad_data + c.to_bytes(1, "little") + xor(known_suffix[1:], s)
        
        json_send(r, {"option": "message", "data": curr_bruteforce_data.hex()})
        curr_hash = json_recv(r)["hash"]

        if curr_hash == curr_valid_hash:
            break
    else:
        raise Exception("BAD")

    found_char = (known_suffix[0] ^ c).to_bytes(1, "little")

    s = found_char + s
    print(s)
        
r.close()

