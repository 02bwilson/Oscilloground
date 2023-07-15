from PyQt6.QtWidgets import QApplication

from Widgets.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    window.show()

    app.exec()