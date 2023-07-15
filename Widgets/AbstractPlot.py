import pyqtgraph as pg
from PyQt6.QtWidgets import QGridLayout, QWidget


class AbstractPlot(QWidget):

    def __init__(self):
        super().__init__()

        self.mainGridLayout = QGridLayout()

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.plotLine = self.graphWidget.plot([0])

        self.plotLine.setData([0])
        self.mainGridLayout.addWidget(self.graphWidget, 0, 0)

        self.setLayout(self.mainGridLayout)

    def plot(self, xData, yData):
        self.plotLine.setData(yData, xData)