import random

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from .handlers.config_handler import ConfigHandler
from .sockets import start_accepting_socket_thread, start_connecting_socket_thread


class FormWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(ConfigHandler.main_form_file, self)

        self.state = False
        self.color = self.color_randomizer()
        self.host_address = ConfigHandler.host_address
        self.button_send.clicked.connect(self.send)
        self.button_host.clicked.connect(self.set_port)
        self.button_host.clicked.connect(self.set_name)
        self.button_host.clicked.connect(self.host)
        self.button_connect.clicked.connect(self.set_port)
        self.button_connect.clicked.connect(self.set_name)
        self.button_connect.clicked.connect(self.set_client_address)
        self.button_connect.clicked.connect(self.connect)

    def keyPressEvent(self, event) -> None:
        if event.key() == ConfigHandler.enter_key:
            self.send()

    def host(self) -> None:
        if self.state:
            return

        self.state = not self.state
        start_accepting_socket_thread(
            address=self.host_address,
            port=self.port,
            instance=self
        )

    def connect(self) -> None:
        if self.state:
            return

        self.state = not self.state
        start_connecting_socket_thread(
            address=self.client_address,
            port=self.port,
            instance=self
        )

    def set_port(self) -> None:
        port = self.port_field.text()
        self.port = int(port)

    def set_client_address(self) -> None:
        self.client_address = self.host_field.text()

    def set_name(self) -> None:
        self.name = self.name_field.text()

    def send(self) -> None:
        message = self.message_field.text()
        self.message_field.clear()

        if not message or not self.state:
            return

        message = ConfigHandler.message.format(
            self.color, self.name, message
        )
        self.communication_socket.send(
            message.encode(
                ConfigHandler.charset
            )
        )
        self.send_user_message(
            message
        )

    def send_user_message(self, message: str) -> None:
        self.chat_field.insertHtml(
            message
        )
        self.chat_field.moveCursor(
            uic.properties.QtGui.QTextCursor.End
        )

    def color_randomizer(self) -> str:
        random_number = random.randint(0, 0xFFFFFF)
        random_hex = hex(random_number)

        return f'#{random_hex[2:]}'
