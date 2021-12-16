import socket

from Crypto.Cipher import AES

MODE = AES.MODE_EAX


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
            f'new connection from: {client_ip}\n'
        )

        while True:
            data = client_socket.recv(16384)

            if not data:
                continue

            aes_message, nonce = data.split(
                config.delimiter.encode(config.charset)
            )

            decrypter = AES.new(client_session_key, MODE, nonce)
            message = decrypter.decrypt(aes_message)

            instance.send_user_message(
                message.decode(config.charset)
            )
