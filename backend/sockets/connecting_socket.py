import socket
from time import time

from loguru import logger
from Crypto.Cipher import AES

from .utils import generate_hash, generate_byte_string

MODE = AES.MODE_EAX


@logger.catch
def create_connection_socket(address: str, port: int) -> socket.socket:
    connection_socket = socket.socket()
    connection_socket.connect(
        (address, port)
    )

    return connection_socket


@logger.catch
def start_connecting_socket(address: str, port=None, instance=None) -> None:
    client_time = time()
    random_bytes = None
    config = instance.config
    delimiter = config.delimiter
    client_hash = generate_hash(
        config=config, time=client_time
    )
    data = f'{client_time}{delimiter}{client_hash}'

    temporary_socket = create_connection_socket(
        address=address, port=config.basic_port
    )
    temporary_socket.send(data.encode(config.charset))

    while True:
        data = temporary_socket.recv(16384)

        if not data:
            continue

        name_socket_port, r_bytes = data.split(
            delimiter.encode(config.charset)
        )
        random_bytes = r_bytes

        temporary_socket.close()
        break

    client_time = time()
    client_name = instance.name
    client_key = instance.public_key.publickey().export_key()
    client_hash = generate_hash(
        config=config, time=client_time, message=random_bytes
    )
    data = generate_byte_string(
        [client_time, client_hash, client_name, client_key], config.delimiter, config.charset
    )

    temporary_socket = create_connection_socket(
        address=address, port=int(name_socket_port)
    )
    temporary_socket.send(data)

    while True:
        data = temporary_socket.recv(16384)

        if not data:
            continue

        rsa_session_key, connection_socket_port = data.split(
            delimiter.encode(config.charset)
        )

        temporary_socket.close()
        break

    session_key = instance.encryptor.decrypt(rsa_session_key)
    instance.session_key = session_key

    temporary_socket = create_connection_socket(
        address=address, port=int(connection_socket_port)
    )
    instance.communication_socket = temporary_socket

    while True:
        try:
            data = temporary_socket.recv(16384)
        except Exception:
            break

        if not data:
            continue

        aes_data, nonce = data.split(
            delimiter.encode(config.charset)
        )
        decrypter = AES.new(session_key, MODE, nonce)
        data = decrypter.decrypt(aes_data)

        instance.send_user_message(
            data.decode(config.charset)
        )
