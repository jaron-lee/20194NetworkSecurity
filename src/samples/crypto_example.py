from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

test_key = bytes.fromhex('00112233445566778899AABBCCDDEEFF')

aesCipher = Cipher(algorithms.AES(test_key), modes.ECB(), backend=default_backend())

aesEnc = aesCipher.encryptor()
aesDec = aesCipher.decryptor()

import sys

file_path = "../../topsecret.bmp"
out_path = "../../lol.bmp"

with open(file_path, "rb") as f:
    data = bytearray(f.read())
    header = data[:54]

    body = data[54:]

    length = len(body)
    to_add = 16 - length % 16
    body += bytearray([0] * to_add)
    new_length = len(body)
    print(new_length % 16)


    with open(out_path, "wb+") as o:
        o.write(header + aesEnc.update(body))
