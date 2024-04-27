#!/usr/bin/env python3

from os import urandom


FLAG = b'crypto{?????????????????????????????}'


def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])


class ChaCha20:
    def __init__(self):
        self._state = []

    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))

    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)

    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1

        for i in range(0, len(m), 64):
            self._setup_state(key, iv)
            for j in range(10):
                self._inner_block(self._state)
            c += xor(m[i:i+64], words_to_bytes(self._state))

            self._counter += 1
        
        return c
    

def _inner_block_inv(state):
    _quarter_round_inv(state, 3, 4, 9, 14)
    _quarter_round_inv(state, 2, 7, 8, 13)
    _quarter_round_inv(state, 1, 6, 11, 12)
    _quarter_round_inv(state, 0, 5, 10, 15)
    _quarter_round_inv(state, 3, 7, 11, 15)
    _quarter_round_inv(state, 2, 6, 10, 14)
    _quarter_round_inv(state, 1, 5, 9, 13)
    _quarter_round_inv(state, 0, 4, 8, 12)
    
def _quarter_round_inv(x, a, b, c, d):
    x[b] = rotate(x[b], 32 - 7)
    x[b] ^= x[c]
    x[c] = word(x[c] - x[d])
    x[d] = rotate(x[d], 32 - 8)
    x[d] ^= x[a]
    x[a] = word(x[a] - x[b])
    x[b] = rotate(x[b], 32 - 12)
    x[b] ^= x[c]
    x[c] = word(x[c] - x[d])
    x[d] = rotate(x[d], 32 - 16)
    x[d] ^= x[a]
    x[a] = word(x[a] - x[b])

msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
iv1 = bytes.fromhex('e42758d6d218013ea63e3c49')
iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')
flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')

state_at_end = bytes_to_words(xor(msg, msg_enc))

for j in range(10):
    _inner_block_inv(state_at_end)

found_key = state_at_end[4:12]
found_key = words_to_bytes(found_key)

c = ChaCha20()
flag_dec = c.encrypt(flag_enc, found_key, iv2)
print(flag_dec)
