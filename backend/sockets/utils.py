import hmac
import binascii

from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP


def generate_hash(config, time, message=None):
    if type(time) in (float, int):
        time = str(time)
        time = time.encode(config.charset)
    elif type(time) is str:
        time = time.encode(config.charset)

    data = time + config.super_key.encode(config.charset)
    key = config.key.encode(config.charset)
    hmac_digest = hmac.digest(
        msg=message or data,
        key=key,
        digest=config.digest
    )

    return binascii.hexlify(hmac_digest).decode()


def generate_byte_string(data: list, delimiter: str, charset: str) -> bytes:
    first = data.pop(0)
    if type(first) in (int, float):
        first = str(first).encode(charset)
    elif type(first) is str:
        first = first.encode(charset)

    delimiter = delimiter.encode(charset)

    while data:
        first += delimiter
        element = data.pop(0)
        if type(element) in (int, float):
            element = str(element).encode(charset)
        elif type(element) is str:
            element = element.encode(charset)
        first += element

    return first


get_random_bytes = get_random_bytes
PKCS1_OAEP = PKCS1_OAEP
