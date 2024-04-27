from pwn import * # pip install pwntools
import json
import base64
import codecs
import Crypto.Util.number

r = remote('socket.cryptohack.org', 13399, level = 'debug')

def recv():
    line = r.recvline()
    return line

def recvjson():
    line = json.loads(r.recvline().decode())
    return line

def sendjson(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


level = 0

received = recv()
print(received)

while True:
    found = False
    
    for i in range(0, 0xFF+1):
        pad = i.to_bytes(1, "little").hex()
        sendjson({"option": "reset_password", "token": pad*32 + pad*64})
        recv = recvjson()
        if recv["msg"] != "Password has been correctly reset.":
            print("BAD")
            break
        
        sendjson({"option": "authenticate", "password": ""})
        recv = recvjson()
        if "Welcome admin" in recv["msg"]:
            print(recv["msg"])
            found = True
            break

    if found:
        break
    
    sendjson({"option": "reset_connection"})
    recv = recvjson()
    if recv["msg"] != "Connection has been reset.":
        print("BAD")
        break
    

r.close()
