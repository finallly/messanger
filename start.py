import sys
from PyQt5 import QtWidgets

from backend.main import FormWindow

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    window = FormWindow()
    window.show()
    sys.exit(application.exec_())
