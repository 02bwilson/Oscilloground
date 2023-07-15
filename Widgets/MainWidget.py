import threading

import qdarktheme
from PyQt6.QtCore import QThread

from PyQt6.QtWidgets import QWidget, QGridLayout

from DataManager import DataManager
from Widgets.AddSignal import AddSignal
from Widgets.FFTPlot import FFTPlot
from Widgets.SignalTable import SignalTable
from Widgets.TimePlot import TimePlot


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Setup vars
        self.mainGridLayout = QGridLayout()

        self.timePlot = TimePlot()
        self.fftPlot = FFTPlot()
        self.signalTable = SignalTable()
        self.addSignalMenu = AddSignal()
        self.dataManager = DataManager()

        self.addSignalMenu.addSignalSignal.connect(self.dataManager.addSignal)
        self.addSignalMenu.addSignalSignal.connect(self.signalTable.signalAdded)

        self.dataThread = QThread()
        self.dataManager.moveToThread(self.dataThread)
        self.dataThread.started.connect(self.dataManager.startGatherData)
        self.dataThread.start()

        self.signalTable.addSignalButton.pressed.connect(self.addSignalMenu.show)

        self.dataManager.newTimeData.connect(self.timePlot.plot)
        self.dataManager.newFFTData.connect(self.fftPlot.plot)

        self.mainGridLayout.addWidget(self.timePlot)
        self.mainGridLayout.addWidget(self.fftPlot, 2, 0)
        self.mainGridLayout.addWidget(self.signalTable, 3, 0)

        qdarktheme.setup_theme("dark")

        self.setLayout(self.mainGridLayout)
