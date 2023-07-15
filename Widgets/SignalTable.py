from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableView, QHeaderView, QAbstractItemView, QPushButton


class SignalTable(QWidget):
    _PLUS_ICON_PATH = "../Content/plus.png"
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
        self.tableModel.setHorizontalHeaderLabels(['ADD/REMOVE ICON', 'DESC'])

        self.tableView.setStyleSheet("background-color: transparent; border:none;")
        self.tableView.setModel(self.tableModel)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.mainGridLayout.addWidget(self.tableView, 0, 0)

        self.tableModel.appendRow([QStandardItem("Base"), QStandardItem("1")])

        self.addSignalButton.setStyleSheet("border:none; text-align:center; color: green; font-size: 24pt;")
        self.addSignalButton.setText("+")
        self.mainGridLayout.addWidget(self.addSignalButton, 1, 0)
