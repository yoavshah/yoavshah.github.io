from pwn import *
import json
import base64
import hashlib

r = remote('socket.cryptohack.org', 13393)#, level = 'debug')

_ = r.recvline()
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)




r.close()



