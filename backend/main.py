import socket
from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from .config_handler import ConfigHandler


class FormWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(ConfigHandler.main_form_file, self)

        self.state = None
        self.host_address = '0.0.0.0'
        self.button_send.clicked.connect(self.send)
        self.button_host.clicked.connect(self.start_listen)
        self.button_connect.clicked.connect(self.start_connection)

    def keyPressEvent(self, event) -> None:
        if event.key() == ConfigHandler.enter_key:
            self.send()

    def start_listen(self) -> None:
        if not self.state:
            self.state = 'host'
            thread = Thread(target=self.host)
            thread.start()

    def host(self) -> None:
        port = int(self.port_line.text())
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )
        server_socket.bind(
            (self.host_address, port)
        )
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            self.communication_socket = client_socket
            self.chat_field.insertHtml(
                ConfigHandler.new_connection_message.format(
                    client_address[0]
                )
            )

            while True:
                request = client_socket.recv(4096)

                if not request:
                    break

                self.chat_field.insertHtml(
                    ConfigHandler.client_message.format(
                        'client', request.decode()
                    )
                )

            client_socket.close()

    def start_connection(self) -> None:
        if not self.state:
            self.state = 'client'
            thread = Thread(target=self.connect)
            thread.start()

    def connect(self) -> None:
        connection_address = self.host_line.text()
        connection_port = int(self.port_line.text())
        self.communication_socket = socket.socket()
        self.communication_socket.connect(
            (connection_address, connection_port)
        )

        while True:
            request = self.communication_socket.recv(4096)

            if not request:
                continue

            self.chat_field.insertHtml(
                ConfigHandler.host_message.format(
                    'host', request.decode()
                )
            )

    def send(self) -> None:
        message = self.message_line.text()
        if message:
            self.communication_socket.send(message.encode('utf-8'))
            if self.state == 'host':
                self.chat_field.insertHtml(
                    ConfigHandler.host_message.format(
                        'host', message
                    )
                )
            else:
                self.chat_field.insertHtml(
                    ConfigHandler.client_message.format(
                        'client', message
                    )
                )
            self.message_line.clear()
