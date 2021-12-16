import random

from Crypto.Cipher import AES
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from Crypto.PublicKey import RSA

from .sockets.utils import PKCS1_OAEP
from .sockets.utils import generate_byte_string
from .handlers.config_handler import ConfigHandler
from .handlers.socket_handler import SocketHandler


class FormWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(ConfigHandler.main_form_file, self)

        self.state = False
        self.clients_mapping = {}
        self.config = ConfigHandler()
        self.socket_handler = SocketHandler()
        self.host_address = self.config.host_address

        self.color_randomizer()
        self.prepare_byte_data()

        self.button_disconnect.hide()
        self.button_disconnect.clicked.connect(self.disconnect)

        self.button_send.clicked.connect(self.send)

        self.button_host.clicked.connect(self.set_port)
        self.button_host.clicked.connect(self.host)

        self.button_connect.clicked.connect(self.set_port)
        self.button_connect.clicked.connect(self.set_client_address)
        self.button_connect.clicked.connect(self.connect)

    def keyPressEvent(self, event) -> None:
        if event.key() == ConfigHandler.enter_key:
            self.send()

    def host(self) -> None:
        if self.state:
            return

        self.set_name()

        self.state = 'host'
        self.socket_handler.start_basic_socket_thread(
            address=self.host_address,
            port=self.config.basic_port,
            instance=self
        )
        self.socket_handler.start_name_socket_thread(
            address=self.host_address,
            port=self.name_socket_port,
            instance=self
        )
        self.socket_handler.start_accepting_socket_thread(
            address=self.host_address,
            port=self.chat_socket_port,
            instance=self
        )

    def connect(self) -> None:
        if self.state:
            return

        self.set_name()

        self.state = 'client'
        self.socket_handler.start_connecting_socket_thread(
            address=self.client_address,
            instance=self
        )
        self.button_connect.hide()
        self.button_disconnect.show()

    def disconnect(self) -> None:
        self.communication_socket.close()
        self.button_disconnect.hide()
        self.button_connect.show()

    def set_port(self) -> None:
        self.name_socket_port = random.randint(10000, 60000)
        self.chat_socket_port = random.randint(10000, 60000)

    def prepare_byte_data(self) -> None:
        key_pair = RSA.generate(3072)
        self.private_key = key_pair
        self.public_key = key_pair.public_key()
        self.encryptor = PKCS1_OAEP.new(key_pair)

    def set_client_address(self) -> None:
        self.client_address = self.host_field.text()

    def set_name(self) -> None:
        self.name = self.name_field.text()

    def send(self) -> None:
        message = self.message_field.text()
        self.message_field.clear()

        if not message or not self.state:
            return

        if self.state == 'client':
            message = ConfigHandler.message.format(
                self.color, self.name, message
            )

            aes_encryptor = AES.new(self.session_key, AES.MODE_EAX)
            aes_text = aes_encryptor.encrypt(
                message.encode(self.config.charset)
            )
            byte_message = generate_byte_string(
                [aes_text, aes_encryptor.nonce], self.config.delimiter, self.config.charset
            )

            self.communication_socket.send(
                byte_message
            )

        if self.state == 'host':
            message = ConfigHandler.message.format(
                self.color, self.name, message
            )
            for client in self.clients_mapping.values():
                aes_encryptor = AES.new(client['session_key'], AES.MODE_EAX)
                aes_text = aes_encryptor.encrypt(
                    message.encode(self.config.charset)
                )
                byte_message = generate_byte_string(
                    [aes_text, aes_encryptor.nonce], self.config.delimiter, self.config.charset
                )

                client['socket'].send(
                    byte_message
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

    def color_randomizer(self):
        random_number = random.randint(0, 0xFFFFFF)
        random_hex = hex(random_number)
        self.color = f'#{random_hex[2:]}'
