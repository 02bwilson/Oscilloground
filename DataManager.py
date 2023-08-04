import math
import threading
import time

import scipy

from PyQt6.QtCore import pyqtSignal, QObject



class DataManager(QObject):
    _TIME_SCALE_FACTOR = 1.0

    _IIR_ALPHA = .999

    _SAMPLE_RATE = 32

    _MOD_VAL = 12.56637061

    _FUNCTION_MAP = {
        "sin": "math.sin",
        "cos": "math.cos",
        "square": "scipy.signal.square",
        "sawtooth": "scipy.signal.sawtooth",
        "triangle": "scipy.signal.triang",
        "constant": "1+"

    }

    newTimeData = pyqtSignal(list, list, int)
    newFFTData = pyqtSignal(list, list, int)

    def __init__(self):

        """
        The __init__ function is called when the class is instantiated.

        :param self: Represent the instance of the class
        :return: Instance of the class
        """
        super().__init__()

        self.startTime = time.time()

        self.continueFlag = True

        self.functions = dict()

        self.dataThread = threading.Thread(target=self.startDataGather)
        self.dataThread.daemon = True
        self.dataThread.start()

        self.dataList = [[], []]

        self.iirData = []

        self.timeList = []

        self.prevCaptureFlag = False

    def setSpeed(self, speed):
        self._TIME_SCALE_FACTOR = speed

    def setMod(self, mod):
        self._MOD_VAL = mod
    def startDataGather(self):
        while (self.continueFlag):
            time.sleep(float(1 / self._SAMPLE_RATE))
            self.gatherData()
            while not self.prevCaptureFlag:
                pass

    def gatherData(self):

        """
        The gatherData function is the main function of this class. It gathers data from the functions
        that are passed to it, and then emits signals with that data. The first signal is a time domain
        signal, which contains the raw values of each sample in a list called self.dataList[0].

        :param self: Access the class attributes
        :return: None - emits new data signal
        """
        now = time.time() - self.startTime
        curVal = 1
        for fn in self.functions.values():
            curVal = eval(str(curVal) + fn[0] + str(fn[1]((now % self._MOD_VAL) * (self._TIME_SCALE_FACTOR))))
        if len(self.dataList[0]) == self._SAMPLE_RATE:
            self.dataList[0].pop(0)
            self.timeList.pop(0)
        self.dataList[0] += [curVal]
        self.timeList += [now]

        self.dataList[1] = scipy.fft.fftshift(scipy.fft.fft(self.dataList[0]))
        self.dataList[1] = [10 * math.log10((v.real * v.real) + (v.imag * v.imag)) if (v.real != 0 and v.imag != 0) else 1
                            for v in self.dataList[1]]
        if len(self.iirData) <= self._SAMPLE_RATE:
            self.iirData = self.dataList[1]
        else:
            for i in range(len(self.iirData)):
                self.iirData[i] = (self.iirData[i] * self._IIR_ALPHA) + (self.dataList[1][i] * (1 - self._IIR_ALPHA))

        self.newFFTData.emit(self.iirData[1:],
                             [(i - (self._SAMPLE_RATE / 2)) for i in range(len(self.dataList[1]))][1:],
                             self._SAMPLE_RATE)

        self.newTimeData.emit(self.dataList[0], self.timeList, self._SAMPLE_RATE)

        self.prevCaptureFlag = True

    def addSignal(self, data):
        """
        The addSignal function takes a dictionary as an argument. The dictionary must contain the following keys:
        name - A string that will be used to id             entify the signal.
        operator - A string representing one of the four basic arithmetic operators (+, -, *, /). This is how this signal will interact with others.
        alpha - A float or integer value that scales this function's output by some factor (e.g., 2*sin(x) would have an alpha of 2).
        beta  - A float or integer value that scales this function's input by some factor (e.g., sin(2x) would have a beta of 2).
        gamma - A float or integer value that changes the phase of this function's input by some factor (e.g., sin(x+2) would have a gamma of 2).

        :param self: Access the functions dictionary
        :param data: Store the information about the signal
        :return: A list of the operator, and a lambda function that is used to calculate the value
        """
        self.functions[data["name"]] = [data["operator"],
                                        lambda t: eval(str(data["alpha"]) + "*" + self._FUNCTION_MAP[data["function"]] \
                                                       + "(" + str(data["beta"]) + "*" + str(t) + "+" + str(
                                            data["gamma"]) + ")")]

    def removeSignal(self, signalName):

        """
        The removeSignal function removes a signal from the list of signals that are being monitored.

        :param self: Represent the instance of the class
        :param signalName: Identify the signal to be removed
        :return: None
        """
        functions = self.functions.keys()
        for fnName in functions:
            if fnName == signalName:
                self.functions.pop(fnName)
