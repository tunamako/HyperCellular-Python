from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random

class CellularController(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.model = self.parent().model

		self.states = [
			QColor(255, 255, 255, 255),
			QColor(0, 0, 0, 255),
		]

		self.initSideCountInput()
		self.initAdjCountInput()
		self.initDepthInput()

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.sideCountLayout)
		self.vbox.addLayout(self.adjCountLayout)
		self.vbox.addLayout(self.depthLayout) 

		randButton = QPushButton()
		nextButton = QPushButton()
		randButton.clicked.connect(self.randomize)
		nextButton.clicked.connect(self.next)
		randButton.setText("Randomize")

		self.vbox.addWidget(randButton)
		self.vbox.addWidget(nextButton)
		self.vbox.addStretch(1)
		self.setLayout(self.vbox)

	def initSideCountInput(self):
		self.sideCountInput = QSpinBox()
		self.sideCountInput.setRange(3, 99)
		self.sideCountInput.setValue(self.model.sideCount)
		self.sideCountInput.valueChanged.connect(self.setSideCount)

		self.sideCountLayout = QHBoxLayout()
		self.sideCountLayout.addWidget(QLabel("Side Count"))
		self.sideCountLayout.addWidget(self.sideCountInput)

	def initAdjCountInput(self):
		self.adjCountInput = QSpinBox()
		self.adjCountInput.setRange(3, 99)
		self.adjCountInput.setValue(self.model.adjacentCount)
		self.adjCountInput.valueChanged.connect(self.setAdjCount)

		self.adjCountLayout = QHBoxLayout()
		self.adjCountLayout.addWidget(QLabel("Adjacency Count"))
		self.adjCountLayout.addWidget(self.adjCountInput)

	def initDepthInput(self):
		self.depthInput = QSpinBox()
		self.depthInput.setRange(1, 99)
		self.depthInput.setValue(self.model.renderDepth)
		self.depthInput.valueChanged.connect(self.setRenderDepth)

		self.depthLayout = QHBoxLayout()
		self.depthLayout.addWidget(QLabel("Render Depth"))
		self.depthLayout.addWidget(self.depthInput)

	def setSideCount(self, count):
		current = self.model.sideCount
		if self.model.setSideCount(count) == -1:
			self.sideCountInput.setValue(current)

	def setAdjCount(self, count):
		current = self.model.adjacentCount
		if self.model.setAdjCount(count) == -1:
			self.adjCountInput.setValue(current)

	def setRenderDepth(self, depth):
		self.model.setRenderDepth(depth)

	def randomize(self):
		for tile in self.model.tiles:
			tile.nextColor = random.choice(self.states)
			self.model.toBeUpdated.append(tile)
		self.model.update()

	def next(self):
		pass