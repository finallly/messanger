import threading

from loguru import logger

from ..sockets import start_basic_socket, start_name_socket, start_connecting_socket, \
    start_accepting_socket


class SocketHandler(object):

    @logger.catch
    def start_socket_thread(self, socket_function, address, instance, port=None) -> None:
        thread = threading.Thread(
            target=socket_function,
            args=[
                address, port, instance
            ]
        )
        thread.start()

    @logger.catch
    def start_basic_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_basic_socket, address, instance, port
        )

    @logger.catch
    def start_name_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_name_socket, address, instance, port
        )

    @logger.catch
    def start_connecting_socket_thread(self, address: str, instance) -> None:
        self.start_socket_thread(
            start_connecting_socket, address, instance
        )

    @logger.catch
    def start_accepting_socket_thread(self, address: str, instance, port: int) -> None:
        self.start_socket_thread(
            start_accepting_socket, address, instance, port
        )
