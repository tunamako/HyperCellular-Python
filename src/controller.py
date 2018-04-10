from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QCheckBox, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QPoint, QTimer

from automaton import Life, WireWorld
import random
import time

class CellularController(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.model = self.parent().model
		self.automaton = WireWorld()
		self.toggleFill()
		
		#self.resetTiles()
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextGeneration)
		self.animSpeed = 100

		self.vbox = QVBoxLayout()
		self.initAnimationButtons()
		self.initSpinBoxes()
		self.initControlButtons()

		self.vbox.addStretch(1)
		self.setLayout(self.vbox)

	def initAnimationButtons(self):
		buttons = [
			#Label, connected function
			["Start", lambda: self.timer.start(self.animSpeed)],
			["Stop", self.timer.stop],
			["Step", self.nextGeneration],
		]

		hbox = QHBoxLayout()

		for button in buttons:
			widget = QPushButton(button[0])
			widget.clicked.connect(button[1])
			hbox.addWidget(widget)

		self.vbox.addLayout(hbox)

	def initSpinBoxes(self):
		self.spinboxes = [
			#Label, min value, max value, init, connected function
			["Speed (ms)", 1, 100000, self.animSpeed, self.setSpeed], 
			["Side Count", 3, 99, self.model.sideCount, self.setSideCount], 
			["Adjacency Count", 3, 99, self.model.adjacentCount, self.setAdjCount],
			["Render Depth", 1, 99, self.model.renderDepth, self.setRenderDepth],
		]

		for i, box in enumerate(self.spinboxes):
			widget = QSpinBox()
			widget.setRange(box[1], box[2])
			widget.setValue(box[3])
			widget.valueChanged.connect(box[4])

			layout = QHBoxLayout()
			layout.addWidget(QLabel(box[0]))
			layout.addWidget(widget)
			self.vbox.addLayout(layout)
			self.spinboxes[i] = widget

	def initControlButtons(self):
		buttons = [
			#Label, connected function
			["Clear", self.resetTiles],
			["Randomize", self.randomize],
			["Toggle Fill", self.toggleFill],
		]

		for button in buttons:
			widget = QPushButton(button[0])
			widget.clicked.connect(button[1])
			self.vbox.addWidget(widget)

	def nextGeneration(self):
		self.automaton.nextGeneration(self.model)
		self.model.updateTiles()

	def setSpeed(self, speed):
		self.animSpeed = speed
		self.timer.setInterval(speed)

	def setSideCount(self, count):
		current = self.model.sideCount

		#If the input is invalid, set the spinbox value to what it was previously
		if self.model.setSideCount(count) == -1:
			self.spinboxes[1].setValue(current)

	def setAdjCount(self, count):
		current = self.model.adjacentCount

		#If the input is invalid, set the spinbox value to what it was previously
		if self.model.setAdjCount(count) == -1:
			self.spinboxes[2].setValue(current)

	def setRenderDepth(self, depth):
		self.model.setRenderDepth(depth)

	def resetTiles(self):
		self.automaton.fill(self.model.tiles)
		self.model.updateTiles()

	def randomize(self):
		self.automaton.randomize(self.model.tiles)
		self.model.updateTiles()

	def toggleFill(self):
		self.model.toggleFillMode()

	def clicked(self, e):
		location = QPoint(e.x(), e.y())
		for tile in self.model.tiles:
			if tile.region.contains(location):
				self.automaton.clicked(tile)
				self.model.updateTiles()
				break