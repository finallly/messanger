import threading

from ..sockets import start_basic_socket, start_name_socket, start_connecting_socket, \
    start_accepting_socket


class SocketHandler(object):

    def start_socket_thread(self, socket_function, address, instance, port=None) -> None:
        thread = threading.Thread(
            target=socket_function,
            args=[
                address, port, instance
            ]
        )
        thread.start()

    def start_basic_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_basic_socket, address, instance, port
        )

    def start_name_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_name_socket, address, instance, port
        )

    def start_connecting_socket_thread(self, address: str, instance) -> None:
        self.start_socket_thread(
            start_connecting_socket, address, instance
        )

    def start_accepting_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_accepting_socket, address, instance, port
        )
