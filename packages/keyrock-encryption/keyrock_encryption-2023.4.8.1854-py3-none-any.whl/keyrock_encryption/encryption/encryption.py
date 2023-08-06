import base64
import hashlib
import json
import re
import string
import random

try:
    from Crypto import Random
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except:
    pass

from keyrock_core import json_util


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = pad(raw.encode(), 16)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:]), 16)

    # def _pad(self, s):
    #     return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    # @staticmethod
    # def _unpad(s):
    #     return s[:-ord(s[len(s)-1:])]


def encrypt_from_json(dict_val: dict, secret_key: str) -> str:
    aes = AESCipher(str(secret_key))
    json_str = json.dumps(dict_val, cls=json_util.CustomEncoder)
    enc_str = aes.encrypt(json_str).decode('utf-8')
    return enc_str


def decrypt_to_json(enc_str: str, secret_key: str) -> dict:
    if enc_str is None:
        return None

    aes = AESCipher(str(secret_key))
    json_str = aes.decrypt(enc_str)
    try:
        dict_val = json.loads(json_str)
    except:
        return json_str

    return dict_val


def encrypt_from_string(str_val, secret_key):
    aes = AESCipher(str(secret_key))
    return aes.encrypt(str_val).decode('utf-8')


def decrypt_to_string(enc_str, secret_key):
    if enc_str is None:
        return None
    aes = AESCipher(str(secret_key))
    return aes.decrypt(enc_str)


def get_random_string(size=16):
    rs = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    return rs
