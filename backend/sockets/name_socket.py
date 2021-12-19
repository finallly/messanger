import socket

from loguru import logger
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from .utils import generate_hash, get_random_bytes, generate_byte_string


def __generate_session_key() -> bytes:
    return get_random_bytes(32)


@logger.catch
def start_name_socket(address: str, port: int, instance):
    config = instance.config
    name_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    name_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )
    name_socket.bind(
        (address, port)
    )
    name_socket.listen()

    while True:
        client_socket, client_address = name_socket.accept()
        client_ip = client_address[0]

        while True:
            data = client_socket.recv(16384)

            if not data:
                break

            client_time, client_hash, client_name, client_public_key = data.split(
                config.delimiter.encode(config.charset)
            )

            random_bytes = instance.clients_mapping[client_ip]
            del instance.clients_mapping[client_ip]

            client_names = [client['name'] for client in instance.clients_mapping.values()]
            if client_name.decode() in client_names:
                break

            host_hash = generate_hash(
                config=config, time=client_time, message=random_bytes
            )

            if host_hash == client_hash.decode():
                client_public_key = RSA.importKey(client_public_key)
                client_encryptor = PKCS1_OAEP.new(client_public_key)
                client_session_key = __generate_session_key()

                rsa_session_key = client_encryptor.encrypt(client_session_key)
                chat_port_value = instance.chat_socket_port
                data = generate_byte_string(
                    [rsa_session_key, chat_port_value], config.delimiter, config.charset
                )

                client_socket.send(
                    data
                )

                instance.clients_mapping[client_ip] = {
                    'name': client_name.decode(),
                    'session_key': client_session_key
                }
