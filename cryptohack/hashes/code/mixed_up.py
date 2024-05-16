from pwn import *
import json
import base64
import hashlib

r = remote('socket.cryptohack.org', 13402)

_ = r.recvline()
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)



# First get the flag length
found = False

for i in range(100):
    zeros_block = b"\x00"*i

    # Validate 3 times because of random
    success_count = 0
    number_of_trials = 5
    for k in range(number_of_trials):

        json_send({"option": "mix", "data": zeros_block.hex()})
        mixed = json_recv()["mixed"]
        +
        for j in range(256):
            data_vector = j.to_bytes(1, "little") * i

            if hashlib.sha256(data_vector).hexdigest() == mixed:
                success_count += 1

    if success_count >= ((number_of_trials * 3) // 5):
        found = True
            
    if found:
        break
    
flag_length = i


print("Flag length = " + str(flag_length))


print("Generating SHA256 vectors")
sha256_vectors = []
for i in range(256):
    h = hashlib.sha256(i.to_bytes(1, "little") * flag_length).hexdigest()
    sha256_vectors.append(h)


number_of_bits = 8 * 39

found_flag = ""
for i in range(number_of_bits):
    b = "0" * i + "1" + "0" * (number_of_bits - i - 1)
    mask_bytes = hex(int(b, base=2))[2:]

    mask_bytes = bytes.fromhex(mask_bytes.zfill(39*2))


    
    success_count = 0
    number_of_trials = 6
    for k in range(number_of_trials):
        json_send({"option": "mix", "data": mask_bytes.hex()})
        mixed = json_recv()["mixed"]
    
        if mixed not in sha256_vectors:
            success_count += 1

    # The current bit in the flag is zero
    if success_count >= ((number_of_trials * 1) // 2):
        found_flag += "1"

    # The current bit in the flag is non zero
    else:
        found_flag += "0"

    print(str(i) + " - " + found_flag)

    flag_chars = ""
    for k in range(0, len(found_flag), 8):
        if len(found_flag[k:k+8]) == 8:
            flag_chars += chr(int(found_flag[k:k+8], 2))

    print(flag_chars)
        

r.close()



