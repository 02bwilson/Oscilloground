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

        self.setStyleSheet("""
        QHeaderView::section {
            background-color: black;
            color: white;
            font: 14px;
        }
        
        QTableView::item {
                    color: white;
                    gridline-color: black;
                    border-color: rgb(242, 128, 133);
                    border: 1px solid white;
                    font: 10px;
        }
        """)

        self.setupTable()

        self.setLayout(self.mainGridLayout)

    def setupTable(self):
        self.tableModel.setHorizontalHeaderLabels(['NAME', 'OPERATOR', 'FUNCTION'])

        self.tableView.setStyleSheet("background-color: transparent; border:none;")
        self.tableView.setModel(self.tableModel)
        self.tableView.verticalHeader().setVisible(False)
        # self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.mainGridLayout.addWidget(self.tableView, 0, 0)

    def signalAdded(self, data):
        fnStr = str(data["alpha"]) + "*" + data["function"] + "(" + str(data["beta"]) + "t" + "+" + str(data["gamma"]) + ")"
        nameItem = QStandardItem(data["name"])
        nameItem.setTextAlignment(Qt.AlignmentFlag .AlignCenter)
        operatorItem = QStandardItem(data["operator"])
        operatorItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        functionItem = QStandardItem(fnStr)
        functionItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tableModel.appendRow([nameItem, operatorItem, functionItem])


    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)

        if a0.key() == Qt.Key.Key_Delete:
            selectedSignalsIndex = self.tableView.selectionModel().currentIndex().row()
            signalName = self.tableModel.item(selectedSignalsIndex, 0).text()
            self.tableModel.removeRow(selectedSignalsIndex)
            self.signalDeleted.emit(signalName)
