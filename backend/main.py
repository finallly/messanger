from subprocess import Popen, PIPE

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from .config_handler import ConfigHandler


class FormWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(ConfigHandler.main_form_file, self)

        self.button_send.clicked.connect(self.send)
        self.button_host.clicked.connect(self.host)
        self.button_connect.clicked.connect(self.connect)

    def keyPressEvent(self, event) -> None:
        self.send()

    def host(self):
        process = Popen(['nc', '-l', '9090'], stdout=PIPE)
        self.chat_field.insertHtml(
            process.stdout.read()
        )

    def connect(self):
        pass

    def send(self):
        self.message_line.clear()
