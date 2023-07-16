import math
import time

import scipy

from PyQt6.QtCore import pyqtSignal, QThread


class DataManager(QThread):
    _IIR_ALPHA = .999

    _SAMPLE_RATE = 64

    _FUNCTION_MAP = {
        "sin": "math.sin",
        "cos": "math.cos",
        "square": "scipy.signal.square",
        "sawtooth": "scipy.signal.sawtooth",
    }

    newTimeData = pyqtSignal(list, list, int)
    newFFTData = pyqtSignal(list, list, int)

    def __init__(self):
        super().__init__()

        self.startTime = time.time()

        self.continueFlag = True

        self.functions = dict()
        self.functions["Example 1"] = ["+", lambda t: math.sin(5 * t)]

        self.dataList = [[], []]

        self.iirData = []

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
        if len(self.dataList[0]) == 4 * self._SAMPLE_RATE:
            self.dataList[0].pop(0)
            self.timeList.pop(0)
        self.dataList[0] += [curVal]
        self.timeList += [now - self.startTime]

        self.dataList[1] = scipy.fft.fftshift(scipy.fft.fft(self.dataList[0]))
        self.dataList[1] = [math.log10((v.real * v.real) + (v.imag * v.imag)) if (v.real != 0 and v.imag != 0) else 1 for v in self.dataList[1]]
        if len(self.iirData) <= 4 * self._SAMPLE_RATE:
            self.iirData = self.dataList[1]
        else:
            for i in range(len(self.iirData)):
                self.iirData[i] = (self.iirData[i] * self._IIR_ALPHA) + (self.dataList[1][i] * (1 - self._IIR_ALPHA))

        self.newFFTData.emit(self.iirData,
                             [(i - (len(self.dataList[1]) / 2)) for i in range(len(self.dataList[1]))],
                             self._SAMPLE_RATE)

        self.newTimeData.emit(self.dataList[0], self.timeList, self._SAMPLE_RATE)

    def addSignal(self, data):
        self.functions[data["name"]] = [data["operator"],
                                        lambda t: eval(str(data["alpha"]) + "*" + self._FUNCTION_MAP[data["function"]] \
                                                       + "(" + str(data["beta"]) + "*" + str(t) + "+" + data["gamma"] + ")")]

    def removeSignal(self, signalName):
        for fnName in self.functions.keys():
            if fnName == signalName:
                self.functions.pop(fnName)
