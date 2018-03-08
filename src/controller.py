from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CellularController(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.model = self.parent().model

		self.vbox = QVBoxLayout()
		self.sideCountLayout = QHBoxLayout()
		self.sideCountInput = QLineEdit()
		self.initInput()

		self.vbox.addLayout(self.sideCountLayout)
		self.setLayout(self.vbox)

	def initInput(self):
		self.sideCountInput.returnPressed.connect(self.setSideCount)
		self.sideCountLabel = QLabel("Side Count")
		self.sideCountLayout.addWidget(self.sideCountLabel)
		self.sideCountLayout.addWidget(self.sideCountInput)

	def setSideCount(self):
		self.model.setSideCount(int(self.sideCountInput.text()))

	def setAdjacentCount(self, adjacentCount):
		pass