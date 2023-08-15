import qdarktheme
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QWidget, QGridLayout, QSizePolicy, QPushButton

from Managers.DataManager import DataManager
from Widgets.AddSignal import AddSignal
from Widgets.FFTPlot import FFTPlot
from Managers.SaveManager import SaveManager
from Widgets.Settings import Settings
from Widgets.SignalTable import SignalTable
from Widgets.TimePlot import TimePlot


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Setup vars
        self.mainGridLayout = QGridLayout()
        self.addSignalButton = QPushButton()
        self.removeSignalButton = QPushButton()

        self.timePlot = TimePlot()
        self.fftPlot = FFTPlot()
        self.signalTable = SignalTable()
        self.addSignalMenu = AddSignal()
        self.dataManager = DataManager()
        self.settings = Settings()
        self.saveManager = SaveManager()

        keys = self.dataManager._FUNCTION_MAP.keys()
        self.addSignalMenu.addFunctions(keys)

        # Add an example signal
        signalData = {"name": "Example_sin_1_t",
                                    "operator": "*",
                                    "function": "sin",
                                    "alpha": 1,
                                    "beta": 1,
                                    "gamma": 0}
        self.dataManager.addSignal(signalData)
        self.signalTable.signalAdded(signalData)

        self.addSignalMenu.addSignalSignal.connect(self.dataManager.addSignal)
        self.addSignalMenu.addSignalSignal.connect(self.signalTable.signalAdded)

        self.settings.settingsDisplay.speedChanged.connect(self.dataManager.setSpeed)
        self.settings.settingsDisplay.modChanged.connect(self.dataManager.setMod)
        self.settings.settingsDisplay.windowSizeChanged.connect(self.dataManager.setWindowSize)
        self.settings.settingsDisplay.iirAlphaChanged.connect(self.dataManager.setIIRAlpha)
        self.settings.settingsDisplay.requestSave.connect(self.saveRequested)
        self.settings.settingsDisplay.requestLoad.connect(self.loadRequested)

        self.signalTable.signalDeleted.connect(self.dataManager.removeSignal)
        self.signalTable.signalDeleted.connect(self.addSignalMenu.removeSignal)

        self.addSignalButton.pressed.connect(self.addSignalMenu.show)

        self.dataManager.newTimeData.connect(self.timePlot.requestPlot)
        self.dataManager.newFFTData.connect(self.fftPlot.requestPlot)

        self.timePlot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mainGridLayout.addWidget(self.timePlot, 0, 0)
        self.fftPlot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mainGridLayout.addWidget(self.fftPlot, 1, 0, 1, 1)

        self.signalTable.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.mainGridLayout.addWidget(self.signalTable, 0, 1, 1, 1)

        self.buttonsLayout = QGridLayout()
        self.buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.addSignalButton.setStyleSheet("border:none; text-align:center; color: green; font-size: 24pt;")
        self.addSignalButton.setText("+")
        self.buttonsLayout.addWidget(self.addSignalButton, 0, 0, Qt.AlignmentFlag.AlignBottom)

        self.removeSignalButton.pressed.connect(self.removePressed)

        self.removeSignalButton.setStyleSheet("border:none; text-align:center; color: red; font-size: 24pt;")
        self.removeSignalButton.setText("-")
        self.buttonsLayout.addWidget(self.removeSignalButton, 1, 0, Qt.AlignmentFlag.AlignBottom)

        self.buttonsLayout.addWidget(self.settings, 2, 0, Qt.AlignmentFlag.AlignBottom)

        self.mainGridLayout.addLayout(self.buttonsLayout, 1, 1, Qt.AlignmentFlag.AlignBottom)

        qdarktheme.setup_theme("dark")

        self.setLayout(self.mainGridLayout)

    def loadRequested(self, path):
        dataList = self.saveManager.load(path)
        for item in dataList:
            self.addSignalMenu.addSignal(item)
    def saveRequested(self, path):
        self.saveManager.save(path, self.dataManager.functions)

    def removePressed(self):
        selectedSignalsIndex = self.signalTable.tableView.selectionModel().currentIndex().row()
        signalName = self.signalTable.tableModel.item(selectedSignalsIndex, 0).text()

        self.signalTable.tableModel.removeRow(selectedSignalsIndex)
        self.signalTable.signalDeleted.emit(signalName)



    def close(self):
        self.settings.close()

        self.dataManager.continueFlag = False

        super().close()