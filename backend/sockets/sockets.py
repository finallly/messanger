import socket
import threading


def create_accepting_socket(address: str, port: int, instance) -> None:
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
        instance.communication_socket = client_socket
        instance.send_user_message(
            f'new connection from: {client_address}'
        )

        while True:
            request = client_socket.recv(8192)

            if not request:
                break

            message = request.decode()
            instance.send_user_message(
                message
            )

        client_socket.close()


def start_accepting_socket_thread(address: str, port: int, instance) -> None:
    thread = threading.Thread(
        target=create_accepting_socket,
        args=[
            address, port, instance
        ]
    )
    thread.start()


def start_connecting_socket(address: str, port: int, instance) -> None:
    communication_socket = socket.socket()
    instance.communication_socket = communication_socket
    communication_socket.connect(
        (address, port)
    )

    while True:
        request = communication_socket.recv(8192)

        if not request:
            continue

        message = request.decode()
        instance.send_user_message(
            message
        )


def start_connecting_socket_thread(address: str, port: int, instance) -> None:
    thread = threading.Thread(
        target=start_connecting_socket,
        args=[
            address, port, instance
        ]
    )
    thread.start()
