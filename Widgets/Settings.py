from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QDialog, QFormLayout, QSlider, QLabel, QLineEdit


class SettingsDisplay(QDialog):
    speedChanged = Signal(float)
    modChanged = Signal(float)
    windowSizeChanged = Signal(float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")

        self.setMinimumSize(300, 300)

        self.mainGridLayout = QGridLayout()

        self.setLayout(self.mainGridLayout)
        self.formLayout = QFormLayout()
        self.mainGridLayout.addLayout(self.formLayout, 0, 0)
        self.setLayout(self.mainGridLayout)
        self.oneTime = 1

        self.speedLabel = QLabel("Speed Mult x1.0")
        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setValue(25)
        self.speedSlider.setMaximum(750)
        self.speedSlider.setMinimum(-74)
        self.speedSlider.valueChanged.connect(self.speedValChanged)
        self.formLayout.addRow(self.speedLabel, self.speedSlider)

        self.windowSizeLabel = QLabel("Window Size x1.0")
        self.windowSizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.windowSizeSlider.setMinimum(-74)
        self.windowSizeSlider.setMaximum(750)
        self.windowSizeSlider.valueChanged.connect(self.windowSizeValueChanged)
        self.formLayout.addRow(self.windowSizeLabel, self.windowSizeSlider)

        self.modLabel = QLabel("Time Modulus 9999")
        self.modEdit = QLineEdit()
        self.modEdit.setValidator(QDoubleValidator())
        self.formLayout.addRow(self.modLabel, self.modEdit)
        self.modEdit.returnPressed.connect(self.modValueChanged)


    def windowSizeValueChanged(self):
        self.windowSizeChanged.emit(round(1.0 + ((-25 + (self.speedSlider.value())) / 100), 3))
    def modValueChanged(self):
        self.modChanged.emit(float(self.modEdit.text()))
    def speedValChanged(self):
        if self.speedSlider.value() >= .95 and self.speedSlider.value() <= 1.05:
            self.speedSlider.setValue(1)
        self.speedLabel.setText("Speed Mult x%s" % str(round(1.0 + ((-25 + (self.speedSlider.value())) / 100), 3)))
        self.speedChanged.emit(round(1.0 + ((-25 + (self.speedSlider.value())) / 100), 3))


class Settings(QWidget):

    def __init__(self):
        super().__init__()

        self.settingsDisplay = SettingsDisplay()

        self.mainGridLayout = QGridLayout()

        self.settingsButton = QPushButton("⚙️")

        self.settingsButton.setStyleSheet("border:none; text-align:center; color: green; font-size: 12pt;")

        self.settingsButton.pressed.connect(self.settingsDisplay.show)
        self.mainGridLayout.addWidget(self.settingsButton, 0, 0)
        self.setLayout(self.mainGridLayout)
