from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QGridLayout, QComboBox, QDialog, QLabel, QLineEdit, QPushButton


class AddSignal(QDialog):
    addSignalSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Signal")

        self.mainGridLayout = QGridLayout()

        self.exampleLabel = QLabel("α * fn(βt+γ)")
        self.nameLabel = QLabel("Name: ")
        self.fnLabel = QLabel("Function: ")
        self.operatorLabel = QLabel("Operator: ")
        self.alphaLabel = QLabel("α: ")
        self.betaLabel = QLabel("β: ")
        self.gammaLabel = QLabel("γ: ")

        self.nameLineEdit = QLineEdit()
        self.alphaLineEdit = QLineEdit()
        self.betaLineEdit = QLineEdit()
        self.gammaLineEdit = QLineEdit()

        self.functionComboBox = QComboBox()
        self.functionComboBox.addItems(["sin", "cos", "square", "sawtooth", "constant"])

        self.operatorComboBox = QComboBox()
        self.operatorComboBox.addItems(["+", "*", "-", "/"])

        self.addButton = QPushButton("Add")
        self.addButton.pressed.connect(self.addSignal)

        self.exampleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exampleLabel.setStyleSheet("text-align: center; font-size:12pt")
        self.mainGridLayout.addWidget(self.exampleLabel, 0, 0, 1, 2)

        self.doubleValidator = QDoubleValidator()
        self.alphaLineEdit.setValidator(self.doubleValidator)
        self.betaLineEdit.setValidator(self.doubleValidator)
        self.gammaLineEdit.setValidator(self.doubleValidator)

        self.mainGridLayout.addWidget(self.nameLabel, 1, 0)
        self.mainGridLayout.addWidget(self.nameLineEdit, 1, 1)

        self.mainGridLayout.addWidget(self.fnLabel, 2, 0)
        self.mainGridLayout.addWidget(self.functionComboBox, 2, 1)

        self.mainGridLayout.addWidget(self.operatorLabel, 3, 0)
        self.mainGridLayout.addWidget(self.operatorComboBox, 3, 1)

        self.mainGridLayout.addWidget(self.alphaLabel, 4, 0)
        self.mainGridLayout.addWidget(self.alphaLineEdit, 4, 1)

        self.mainGridLayout.addWidget(self.betaLabel, 5, 0)
        self.mainGridLayout.addWidget(self.betaLineEdit, 5, 1)

        self.mainGridLayout.addWidget(self.gammaLabel, 6, 0)
        self.mainGridLayout.addWidget(self.gammaLineEdit, 6, 1)

        self.mainGridLayout.addWidget(self.addButton, 99, 0, 1, 2)
        self.setLayout(self.mainGridLayout)

    def addSignal(self):
        data = {"name": self.nameLineEdit.text(),
                "function": self.functionComboBox.currentText(),
                "operator": self.operatorComboBox.currentText(),
                "alpha": self.alphaLineEdit.text(),
                "beta": self.betaLineEdit.text(),
                "gamma": self.gammaLineEdit.text()}

        self.addSignalSignal.emit(data)

        self.close()
