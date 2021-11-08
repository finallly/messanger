import sys
from PyQt5 import QtWidgets

from backend.handlers.config_handler import ConfigHandler
from backend.handlers.file_handler import fileHandler
from backend.main import FormWindow

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    with fileHandler(ConfigHandler.main_qss_file, ConfigHandler.file_in_mode) as file_in:
        application.setStyleSheet(file_in.read())
    window = FormWindow()
    window.show()
    sys.exit(application.exec_())
