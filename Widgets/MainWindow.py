from PyQt6.QtWidgets import QMainWindow

from Widgets.MainWidget import MainWidget

class MainWindow(QMainWindow):
    _MAIN_VERSION = 0x1
    _SUB_VERSION = 0x2
    _VERSION = str(_MAIN_VERSION) + "." + str(_SUB_VERSION)
    def __init__(self):
        super().__init__()

        self.setMinimumSize(250, 250)

        self.setWindowTitle("Oscilloground v%s" % self._VERSION)

        self.widget = MainWidget()

        self.setCentralWidget(self.widget)
