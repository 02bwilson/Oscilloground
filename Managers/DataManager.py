import math
import threading
import time
import random

import scipy

from PyQt6.QtCore import pyqtSignal, QObject


class DataManager(QObject):
    _WINDOW_SIZE = 1

    _TIME_SCALE_FACTOR = 1.5

    _IIR_ALPHA = .9

    _SAMPLE_RATE = 32

    _MOD_VAL = 9999

    _FUNCTION_MAP = {
        "sin": "math.sin",
        "cos": "math.cos",
        "square": "scipy.signal.square",
        "sawtooth": "scipy.signal.sawtooth",
        "triangle": "scipy.signal.triang",
        "constant": "1+",
        "random": "random.random()+"
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

        # Grab the current time so we can measure the time elapsed
        self.startTime = time.time()

        # Flag that allows the data gatherer to continue
        self.continueFlag = True

        self.functions = dict()

        # Start the data thread
        self.dataThread = threading.Thread(target=self.startDataGather)
        self.dataThread.daemon = True
        self.dataThread.start()

        # Place to hold the data,
        self.dataDict = {'time': [],
                         'fft': []}

        # IIR Filter data
        self.iirData = []

        # Place to hold an array of the seconds of the current window
        self.timeList = []

        # Flag to determine if previous data computations have finished
        self.prevCaptureFlag = False

    def setIIRAlpha(self, alpha):
        self._IIR_ALPHA = alpha

    def setSpeed(self, speed):
        self._TIME_SCALE_FACTOR = speed

    def setMod(self, mod):
        self._MOD_VAL = mod

    def setWindowSize(self, windowSize):
        self._WINDOW_SIZE = int(windowSize)

    def startDataGather(self):
        """
        The startDataGather function is the main function that runs in a separate thread.
        It will run until the continueFlag is set to False. The startDataGather function calls gatherData()
        every 1/SAMPLE_RATE seconds, which gathers data from all of the functions stores it in an dict called self.dataDict
        The startDataGather function also checks if prevCaptureFlag has been set to True by another thread (the one running capturePrev).

        :param self: Refer to the object itself
        :return: The data gathered from the gatherdata function
        """
        while (self.continueFlag):
            time.sleep(float(1 / self._SAMPLE_RATE))
            self.gatherData()
            while not self.prevCaptureFlag:
                pass
        return

    def gatherData(self):

        """
        The gatherData function is the main function of this class. It gathers data from the functions
        that are passed to it, and then emits signals with that data. The first signal is a time domain
        signal, which contains the raw values of each sample in a list called self.dataList[0].

        :param self: Access the class attributes
        :return: None - emits new data signal
        """
        # Get the time elapsed
        now = time.time() - self.startTime

        # Start with a base value of 1
        curVal = 1

        # Apply all the functions on the value
        for fn in self.functions.values():
            curVal = eval(str(curVal) + fn[0] + str(fn[1]((now % self._MOD_VAL) * self._TIME_SCALE_FACTOR)))

        # If the window is full pop the oldest value off
        if len(self.dataDict['time']) == self._WINDOW_SIZE * self._SAMPLE_RATE:
            self.dataDict['time'].pop(0)
            self.timeList.pop(0)
        # If the window size has been decreased we need to resize the time data
        elif len(self.dataDict['time']) > self._WINDOW_SIZE * self._SAMPLE_RATE:
            spliceSpot = (len(self.dataDict['time']) - (self._WINDOW_SIZE * self._SAMPLE_RATE))
            self.dataDict['time'] = self.dataDict['time'][int(spliceSpot) + 1:]
        # Add the current value
        self.dataDict['time'] += [curVal]
        self.timeList += [now]

        # Apply FFT & FFT Shift
        self.dataDict['fft'] = scipy.fft.fftshift(scipy.fft.fft(self.dataDict['time']))
        # Get magnitude data
        self.dataDict['fft'] = [
            10 * math.log10((v.real * v.real) + (v.imag * v.imag)) if (v.real != 0 and v.imag != 0) else 1
            for v in self.dataDict['fft']]

        # If the IIR Size is not the desired size then just set all the values
        if len(self.iirData) != self._WINDOW_SIZE * self._SAMPLE_RATE:
            self.iirData = self.dataDict['fft']
        # Else we can apply the IIR formula to all values
        else:
            for i in range(len(self.iirData)):
                self.iirData[i] = (self.iirData[i] * self._IIR_ALPHA) + (
                        self.dataDict['fft'][i] * (1 - self._IIR_ALPHA))
        self.newFFTData.emit(self.iirData[1:],
                             [(i - ((self._SAMPLE_RATE * self._WINDOW_SIZE) / 2)) for i in
                              range(len(self.dataDict['fft']))][1:],
                             self._SAMPLE_RATE)

        # If the window time list is not the right size, resize it.
        if len(self.timeList) > len(self.dataDict['time']):
            self.timeList = self.timeList[len(self.timeList) - len(self.dataDict['time']):]
        self.newTimeData.emit(self.dataDict['time'], self.timeList, self._SAMPLE_RATE)

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
        # Add a function
        # Operator: the operator that will be applied to the curValue
        # Lambda t: A lambda expression representing the signal
        self.functions[data["name"]] = [data["operator"],
                                        lambda t: eval(str(data["alpha"]) + "*" + self._FUNCTION_MAP[data["function"]]
                                                       + "(" + str(data["beta"]) + "*" + str(t) + "+" + str(
                                            data["gamma"]) + ")"), [data["alpha"], data["beta"], data["gamma"],
                                                                    data["function"],
                                                                    self._FUNCTION_MAP[data["function"]]]]

    def removeSignal(self, signalName):
        """
        The removeSignal function removes a signal from the list of signals that are being monitored.

        :param self: Represent the instance of the class
        :param signalName: Identify the signal to be removed
        :return: None
        """
        # Remove the function
        functions = self.functions.keys()
        for fnName in functions:
            if fnName == signalName:
                self.functions.pop(fnName)
