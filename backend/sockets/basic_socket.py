import socket
import threading

from .utils import generate_hash, get_random_bytes, generate_byte_string


def start_basic_socket(address: str, port: int, instance):
    config = instance.config
    basic_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    basic_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )
    basic_socket.bind(
        (address, port)
    )
    basic_socket.listen()

    while True:
        client_socket, client_address = basic_socket.accept()
        client_ip = client_address[0]

        while True:
            data = client_socket.recv(16384)

            if not data:
                break

            client_time, client_hash = data.decode().strip().split(
                config.delimiter)
            name_socket_port = instance.name_socket_port
            host_hash = generate_hash(
                config=config, time=client_time
            )

            if host_hash == client_hash:
                random_bytes = get_random_bytes(32)
                instance.clients_mapping[client_ip] = random_bytes
                data = generate_byte_string(
                    [name_socket_port, random_bytes], config.delimiter, config.charset
                )
                client_socket.send(
                    data
                )

            client_socket.close()
            break


def start_basic_socket_thread(address: str, port: int, instance):
    thread = threading.Thread(
        target=start_basic_socket,
        args=[
            address, port, instance
        ]
    )
    thread.start()
