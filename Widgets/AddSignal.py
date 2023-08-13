from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QGridLayout, QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox


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

        self.signalNameList = list()

        self.functionComboBox = QComboBox()
        self.functionComboBox.addItems(["sin", "cos", "square", "sawtooth", "constant", "random"])

        self.operatorComboBox = QComboBox()
        self.operatorComboBox.addItems(["+", "*", "-", "/"])

        self.addButton = QPushButton("Add")
        self.addButton.pressed.connect(lambda: self.addSignal(None))

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

    def removeSignal(self, signalName):
        if signalName in self.signalNameList:
            self.signalNameList.remove(signalName)

    def addSignal(self, payload):
        data = {"name": self.nameLineEdit.text(),
                "function": self.functionComboBox.currentText(),
                "operator": self.operatorComboBox.currentText(),
                "alpha": self.alphaLineEdit.text(),
                "beta": self.betaLineEdit.text(),
                "gamma": self.gammaLineEdit.text()}

        if payload is not None:
            data = {"name": payload[0],
                    "function": payload[5],
                    "operator": payload[1],
                    "alpha": payload[2],
                    "beta": payload[3],
                    "gamma": payload[4]}

        invalidFlag = False
        if data["name"] in self.signalNameList or data["name"] in ["", None] or '::' in data['name']:
            mbox = QMessageBox()
            mbox.setWindowTitle('Name Error!')
            mbox.setText('There is a problem with the name of your signal!\n\n'
                         'The name cannot be a duplicate, and \n'
                         "it cannot be empty or  contain '::'")
            mbox.exec()
            self.nameLineEdit.setStyleSheet("border: 1px solid red")
            invalidFlag = True
        else:
            self.nameLineEdit.setStyleSheet('border: none;')

        checkArray = ["", None, "."]
        if data["alpha"] in checkArray:
            self.alphaLineEdit.setStyleSheet('border: 1px solid red')
            invalidFlag = True
        else:
            self.alphaLineEdit.setStyleSheet('border: none;')
        if data["beta"] in checkArray:
            self.betaLineEdit.setStyleSheet('border: 1px solid red')
            invalidFlag = True
        else:
            self.betaLineEdit.setStyleSheet('border: none;')
        if data["gamma"] in checkArray:
            self.gammaLineEdit.setStyleSheet('border: 1px solid red')
            invalidFlag = True
        else:
            self.gammaLineEdit.setStyleSheet('border: none;')
        if invalidFlag:
            return

        for lineEdit in [self.nameLineEdit, self.alphaLineEdit, self.betaLineEdit, self.gammaLineEdit]:
            lineEdit.setStyleSheet('border: none')

        self.addSignalSignal.emit(data)

        self.signalNameList.append(data["name"])

        self.close()
