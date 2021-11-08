from backend.handlers.config_handler import ConfigHandler


class fileHandler(object):

    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def __enter__(self):
        self.data = open(self.file, mode=self.mode, encoding=ConfigHandler.charset)
        return self.data

    def __exit__(self, *args):
        self.data.close()
