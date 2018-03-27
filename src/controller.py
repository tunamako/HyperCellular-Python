from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QLabel

from automaton import Automaton
import random

class CellularController(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.model = self.parent().model
		self.automaton = Automaton()


		self.initSideCountInput()
		self.initAdjCountInput()
		self.initDepthInput()

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.sideCountLayout)
		self.vbox.addLayout(self.adjCountLayout)
		self.vbox.addLayout(self.depthLayout) 

		randButton = QPushButton()
		randButton.clicked.connect(self.randomize)
		randButton.setText("Randomize")
		nextButton = QPushButton()
		nextButton.clicked.connect(self.nextGeneration)
		nextButton.setText("Next Gen")

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

		#If the input is invalid, set the spinbox value to what it was previously
		if self.model.setSideCount(count) == -1:
			self.sideCountInput.setValue(current)

	def setAdjCount(self, count):
		current = self.model.adjacentCount

		#If the input is invalid, set the spinbox value to what it was previously
		if self.model.setAdjCount(count) == -1:
			self.adjCountInput.setValue(current)

	def setRenderDepth(self, depth):
		self.model.setRenderDepth(depth)

	def randomize(self):
		self.automaton.randomize(self.model.tiles)
		self.model.updateTiles()

	def nextGeneration(self):
		self.automaton.nextGeneration(self.model.tiles)
		self.model.updateTiles()