from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QDialog, QFormLayout, QSlider, QLabel, QLineEdit, \
    QFileDialog


class SettingsDisplay(QDialog):
    speedChanged = Signal(float)
    modChanged = Signal(float)
    windowSizeChanged = Signal(float)
    iirAlphaChanged = Signal(float)
    requestSave = Signal(str)
    requestLoad = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")

        self.setMinimumSize(300, 300)

        self.mainGridLayout = QGridLayout()

        self.setLayout(self.mainGridLayout)
        self.formLayout = QFormLayout()
        self.mainGridLayout.addLayout(self.formLayout, 0, 0, 1, 2)
        self.setLayout(self.mainGridLayout)
        self.oneTime = 1

        self.speedLabel = QLabel("Speed Mult: 1.0")
        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setValue(25)
        self.speedSlider.setMaximum(750)
        self.speedSlider.setMinimum(-74)
        self.speedSlider.valueChanged.connect(self.speedValChanged)
        self.formLayout.addRow(self.speedLabel, self.speedSlider)

        self.windowSizeLabel = QLabel("Window Size: 1")
        self.windowSizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.windowSizeSlider.setMinimum(1)
        self.windowSizeSlider.setMaximum(10)
        self.windowSizeSlider.valueChanged.connect(self.windowSizeValueChanged)
        self.formLayout.addRow(self.windowSizeLabel, self.windowSizeSlider)

        self.modLabel = QLabel("Time Modulus: 9999")
        self.modEdit = QLineEdit()
        self.modEdit.setValidator(QDoubleValidator())
        self.formLayout.addRow(self.modLabel, self.modEdit)
        self.modEdit.returnPressed.connect(self.modValueChanged)

        self.iirAlphaLabel = QLabel("IIR α: .990")
        self.iirAlphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.iirAlphaSlider.setMinimum(10)
        self.iirAlphaSlider.setMaximum(99)
        self.iirAlphaSlider.setValue(90)
        self.formLayout.addRow(self.iirAlphaLabel, self.iirAlphaSlider)
        self.iirAlphaSlider.valueChanged.connect(self.iirAlphaValueChanged)

        self.saveSignalsButton = QPushButton("Save")
        self.saveSignalsButton.pressed.connect(self.saveButtonPressed)
        self.saveSignalsFileDialog = QFileDialog()
        self.mainGridLayout.addWidget(self.saveSignalsButton, 1, 0)

        self.loadSignalsButton = QPushButton("Load")
        self.loadSignalsButton.pressed.connect(self.loadButtonPressed)
        self.loadSignalsFileDialog = QFileDialog()
        self.mainGridLayout.addWidget(self.loadSignalsButton, 1, 1)


    def saveButtonPressed(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "untitled.ogc", "Oscilloground Config(*.ogc)")
        if file_name:
            self.requestSave.emit(file_name)

    def loadButtonPressed(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "Oscilloground Config(*.ogc)")
        if file_name:
            self.requestLoad.emit(file_name)

    def iirAlphaValueChanged(self):
        val = float(self.iirAlphaSlider.value()) / 100.0
        self.iirAlphaLabel.setText("IIR Alpha: %s" % val)
        self.iirAlphaChanged.emit(val)
    def windowSizeValueChanged(self):
        self.windowSizeLabel.setText("Window Size: " + str(self.windowSizeSlider.value()))
        self.windowSizeChanged.emit(self.windowSizeSlider.value())
    def modValueChanged(self):
        self.modLabel.setText(str(self.modEdit.text()))
        self.modChanged.emit(float(self.modEdit.text()))
    def speedValChanged(self):
        if self.speedSlider.value() >= .95 and self.speedSlider.value() <= 1.05:
            self.speedSlider.setValue(1)
        self.speedLabel.setText("Speed Mult: %s" % str(round(1.0 + ((-25 + (self.speedSlider.value())) / 100), 3)))
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
