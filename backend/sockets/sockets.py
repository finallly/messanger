import socket
from _thread import *
import threading
from loguru import logger


def threaded_client(connection):
    connection.send(str.encode('Omae wa mou shindeiru....'))
    while True:
        request = connection.recv(8192)
        reply = 'Server Says: ' + request.decode('utf-8')
        if not request:
            break
        connection.sendall(str.encode(reply))
    connection.close()


def start_accepting_socket_thread(address: str, port: int, instance) -> None:
    thread_count = 0
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )

    try:
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )
        server_socket.bind(
            (address, port)
        )
        server_socket.listen()

    except socket.error as exc:
        logger.error(str(exc))

    while True:
        client_socket, client_address = server_socket.accept()
        logger.info(f'Connected to: {client_address[0]}:{client_address[1]}')

        start_new_thread(threaded_client, (client_socket, ))
        thread_count += 1
        logger.info(f'Thread Number: {thread_count}')

        instance.communication_socket = client_socket
        instance.send_user_message(
            f'new connection from: {client_address}'
        )

        client_socket.close()


def start_connecting_socket(address: str, port: int, instance) -> None:
    communication_socket = socket.socket()
    instance.communication_socket = communication_socket
    try:
        communication_socket.connect(
            (address, port)
        )

    except socket.error as exc:
        logger.error(str(exc))

    request = communication_socket.recv(8192)

    while True:

        if not request:
            continue

        message = request.decode()
        instance.send_user_message(
            message
        )
