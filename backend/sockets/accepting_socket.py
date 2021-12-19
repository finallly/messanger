import socket

from loguru import logger
from Crypto.Cipher import AES

from .utils import generate_byte_string

MODE = AES.MODE_EAX


@logger.catch
def start_accepting_socket(address: str, port: int, instance) -> None:
    config = instance.config
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    server_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )
    server_socket.bind(
        (address, port)
    )
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        client_session_key = instance.clients_mapping[client_ip]['session_key']
        instance.clients_mapping[client_ip]['socket'] = client_socket

        instance.send_user_message(
            config.new_connection_message.format(client_ip)
        )

        while True:
            try:
                data = client_socket.recv(16384)
            except Exception:
                break

            if not data:
                continue

            aes_message, nonce = data.split(
                config.delimiter.encode(config.charset)
            )

            decrypter = AES.new(client_session_key, MODE, nonce)
            message = decrypter.decrypt(aes_message)

            for client in instance.clients_mapping.values():
                aes_encryptor = AES.new(client['session_key'], AES.MODE_EAX)
                aes_text = aes_encryptor.encrypt(
                    message
                )
                byte_message = generate_byte_string(
                    [aes_text, aes_encryptor.nonce], config.delimiter, config.charset
                )

                client['socket'].send(
                    byte_message
                )

            instance.send_user_message(
                message.decode(config.charset)
            )

        instance.send_user_message(
            config.user_left_message.format(
                instance.clients_mapping[client_ip]['name']
            )
        )

        del instance.clients_mapping[client_ip]
