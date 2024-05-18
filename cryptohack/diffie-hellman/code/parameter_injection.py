from pwn import *
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

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



r = remote('socket.cryptohack.org', 13371, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


b = 197395083814907028991785772714920885908249341925650951555219049411298436217190605190824934787336279228785809783531814507661385111220639329358048196339626065676869119737979175531770768861808581110311903548567424039264485661330995221907803300824165469977099494284722831845653985392791480264712091293580274947132480402319812110462641143884577706335859190668240694680261160210609506891842793868297672619625924001403035676872189455767944077542198064499486164431451944

data = json.loads(r.recvline()[len("Intercepted from Alice: "):])


r.sendline(json.dumps(data).encode())

B = pow(int(data["g"], 16), b, int(data["p"], 16))

shared_secret = pow(int(data["A"], 16), b, int(data["p"], 16))

x = r.recvline()[len("Send to Bob: Intercepted from Bob: "):]
bob_data = json.loads(x)

B_bob = int(bob_data["B"], 16)

# Send the attacker B
r.sendline(json.dumps({"B": hex(B)}).encode())

x = r.recvline()
x = x[x.index(b"{"):]

cipher_flag = json.loads(x)



print(decrypt_flag(shared_secret, cipher_flag["iv"], cipher_flag["encrypted_flag"]))


r.close()



