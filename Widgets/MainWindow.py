from PyQt6.QtWidgets import QMainWindow

from Widgets.MainWidget import MainWidget

class MainWindow(QMainWindow):

    _VERSION = "1.0"
    def __init__(self):
        super().__init__()

        self.setMinimumSize(250, 250)

        self.setWindowTitle("Oscilloground v%s" % self._VERSION)

        self.widget = MainWidget()

        self.setCentralWidget(self.widget)