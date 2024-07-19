import json
from base64 import b64encode

import requests
import rsa.randnum
from Crypto.Cipher import AES
from requests import JSONDecodeError, RequestException
from rsa import PublicKey, encrypt

AUTH_SERVER = 'http://127.0.0.2:8000'
AUTHENTICATE_URL = '/authenticate'
VALIDATE_URL = '/validate'
GET_COUNT_URL = '/get_count'
PUBLIC_KEY = PublicKey(
    7986291780433942702581136058302074301869943192822634967674988332655544673562834902209971777236281808177806213336709918483629434748245227209063301345541661,
    65537)


def encrypt_data(data):
    if isinstance(data, str):
        data = [data]

    cipher_data = []
    tag_data = []
    aes_keys = []
    nonces = []

    # AES encrypt the data
    for item in data:
        aes_key = rsa.randnum.read_random_bits(128)
        cipher = AES.new(aes_key, AES.MODE_OCB)
        item = item.encode()
        ciphertext, tag = cipher.encrypt_and_digest(item)
        e_tag = encrypt(tag, PUBLIC_KEY)
        cipher_data.append(b64encode(ciphertext))
        tag_data.append(b64encode(e_tag))

        # RSA encrypt the AES keys
        aes_keys.append(b64encode(encrypt(aes_key, PUBLIC_KEY)))
        nonces.append(b64encode(encrypt(cipher.nonce, PUBLIC_KEY)))

    return cipher_data, aes_keys, nonces, tag_data


def authenticate(qr_id, qr):
    try:
        e_data, e_key, e_nonce, e_tag = encrypt_data([qr_id, json.dumps(qr)])
        data = {"id": e_data[0], "qr": e_data[1], "id_key": e_key[0], "qr_key": e_key[1], "id_nonce": e_nonce[0],
                "qr_nonce": e_nonce[1], "id_tag": e_tag[0], "qr_tag": e_tag[1]}
        r = requests.post(f"{AUTH_SERVER}{AUTHENTICATE_URL}", data=data)
        authed = r.json()["auth"]
        return authed == "true"
    except (TypeError, JSONDecodeError, RequestException):
        return False


def validate(qr):
    try:
        e_data, e_key, e_nonce, e_tag = encrypt_data(qr)
        data = {"qr": e_data[0], "key": e_key[0], "nonce": e_nonce[0], "tag": e_tag[0]}
        r = requests.post(f"{AUTH_SERVER}{VALIDATE_URL}", data=data)
        valid = r.json()["valid"]
        if valid == "true":
            qr_id = r.json()["qr_id"]
            return qr_id
        else:
            return None
    except (TypeError, JSONDecodeError, RequestException):
        return None


def get_count(qr_id):
    try:
        e_data, e_key, e_nonce, e_tag = encrypt_data(qr_id)
        data = {"id": e_data[0], "key": e_key[0], "nonce": e_nonce[0], "tag": e_tag[0]}
        r = requests.post(f"{AUTH_SERVER}{GET_COUNT_URL}", data=data)
        count = r.json()["count"]
        return count
    except (TypeError, JSONDecodeError, RequestException) as e:
        return -1
