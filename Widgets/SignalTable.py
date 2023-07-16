from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableView, QHeaderView, QAbstractItemView, QPushButton


class SignalTable(QWidget):


    signalDeleted = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Setup vars
        self.mainGridLayout = QGridLayout()
        self.tableView = QTableView()
        self.tableModel = QStandardItemModel()
        self.addSignalButton = QPushButton()

        self.setupTable()

        self.setLayout(self.mainGridLayout)

    def setupTable(self):
        self.tableModel.setHorizontalHeaderLabels(['NAME', 'FUNCTION'])

        self.tableView.setStyleSheet("background-color: transparent; border:none;")
        self.tableView.setModel(self.tableModel)
        self.tableView.verticalHeader().setVisible(False)
        # self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.mainGridLayout.addWidget(self.tableView, 0, 0)

        self.tableModel.appendRow([QStandardItem("Example 1"), QStandardItem("sin(5*t)")])

        self.addSignalButton.setStyleSheet("border:none; text-align:center; color: green; font-size: 24pt;")
        self.addSignalButton.setText("+")
        self.mainGridLayout.addWidget(self.addSignalButton, 1, 0)

    def signalAdded(self, data):
        fnStr = str(data["alpha"]) + "*" + data["function"] + "(" + data["beta"] + "t" + "+" + data["gamma"] + ")"
        nameItem = QStandardItem(data["name"])
        self.tableModel.appendRow([nameItem, QStandardItem(fnStr)])

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)

        if a0.key() == Qt.Key.Key_Delete:
            selectedSignalsIndex = self.tableView.selectionModel().currentIndex().row()
            signalName = self.tableModel.item(selectedSignalsIndex, 0).text()
            self.tableModel.removeRow(selectedSignalsIndex)
            self.signalDeleted.emit(signalName)
