import math
import threading
import time

import scipy

from PyQt6.QtCore import pyqtSignal, QTimer, QThread


class DataManager(QThread):
    _SAMPLE_RATE = 64

    newTimeData = pyqtSignal(list, list, int)
    newFFTData = pyqtSignal(list, list, int)

    def __init__(self):
        super().__init__()

        self.startTime = time.time()

        self.continueFlag = True

        self.functions = dict()
        self.functions["Example 1"] = ["*", lambda t: math.sin(10 * t)]

        self.dataList = [[], []]
        self.timeList = []

    def startGatherData(self):
        while (self.continueFlag):
            time.sleep(1.0 / self._SAMPLE_RATE)
            self.gatherData()

    def gatherData(self):
        now = time.time()
        curVal = 1
        for fn in self.functions.values():
            curVal = eval(str(curVal) + fn[0] + str(fn[1](now)))
        if len(self.dataList[0]) == 8 * self._SAMPLE_RATE:
            self.dataList[0].pop(0)
            self.timeList.pop(0)
        self.dataList[0] += [curVal]
        self.timeList += [now - self.startTime]

        if len(self.dataList[0]) >= 2 * self._SAMPLE_RATE:
            self.dataList[1] = scipy.fft.fftshift(scipy.fft.fft(self.dataList[0]))
            self.dataList[1] = [math.log10((v.real * v.real) + (v.imag * v.imag)) for v in self.dataList[1]]
            self.newFFTData.emit(self.dataList[1],
                                 [(i - (self._SAMPLE_RATE / 2)) for i in range(len(self.dataList[1]))],
                                 self._SAMPLE_RATE)

        self.newTimeData.emit(self.dataList[0], self.timeList, self._SAMPLE_RATE)

    def addSignal(self, data):
        self.functions[data["name"]] = [data["operator"],
                                        lambda t: eval(str(data["alpha"]) + "*" + "scipy." + data["function"] \
                                                       + "(" + str(data["beta"]) + str(t) + "+" + data["gamma"] + ")")]
