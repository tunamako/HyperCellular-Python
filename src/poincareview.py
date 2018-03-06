from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from reflectionaxis import ArcAxis, LineAxis
from math_helpers import areCollinear

import math
from collections import defaultdict
from pprint import *

class PoincareView(QOpenGLWidget):
	def __init__(self):
		super().__init__()
		self.centerVertices = []
		self.origin = QPointF()

		self.drawnCount = 0
		self.drawnTiles = defaultdict(set)
		self.sideCount = 5
		self.adjacentCount = 4
		self.renderLayers = 3

	def genCenterVertices(self):
		p = self.sideCount
		q = self.adjacentCount
		dist = (self.diskDiameter/2) * math.sqrt(math.cos(math.pi/p + math.pi/q)*math.cos(math.pi/q) / (math.sin(2*math.pi/q) * math.sin(math.pi/p) + math.cos(math.pi/p + math.pi/q)* math.cos(math.pi/q)))
		alpha = 2*math.pi/p

		for i in range(p):
			x = self.origin.x() + (dist) * math.cos(i * alpha)
			y = self.origin.y() + (dist) * math.sin(i * alpha)

			self.centerVertices.append(QPointF(x, y))
		
	def hasBeenDrawn(self, aPoint):
		precision = 1000
		x = round(precision * aPoint.x())/precision
		y = round(precision * aPoint.y())/precision

		if x in self.drawnTiles and y in self.drawnTiles[x]:
			return True

		self.drawnTiles[x].add(y)
		return False

	def drawTile(self, vertices, center, layers) :
		reflectedVertices = []
		reflectedCenter = QPointF()

		self.drawnCount += 1
		self.painter.drawPoint(center)

		for i, v in enumerate(vertices):
			A = v
			if i+1 is not len(vertices):
				B = vertices[i+1]
			else:
				B = vertices[0]

			if areCollinear(A, B, self.origin):
				self.painter.drawLine(A, B)
				continue
			else:
				axis = ArcAxis(A, B, self.origin, self.diskDiameter)
				if axis.collinear:
					axis = LineAxis(A, B)

		
			axis.draw(self.painter)

			if layers is 1: continue

			reflectedCenter = axis.reflectPoint(center)
			if self.hasBeenDrawn(reflectedCenter):
				continue
			reflectedVertices = [axis.reflectPoint(j) for j in vertices]

			self.drawTile(reflectedVertices, reflectedCenter, layers - 1) == 0
		
	def paintEvent(self, QPaintEvent):
		self.diskDiameter = min(self.size().width(), self.size().height()) - 10
		self.painter = QPainter(self)
		self.diskPath = QPainterPath()

		self.origin.setX(self.size().width()/2)
		self.origin.setY(self.size().height()/2)

		self.painter.setPen(QPen(QColor(122, 0, 127, 255), 2))

		diskRegion = QRegion(QRect(self.origin.x() - self.diskDiameter/2, self.origin.y() - self.diskDiameter/2, self.diskDiameter, self.diskDiameter), QRegion.Ellipse)
		self.painter.setClipRegion(diskRegion)

		self.genCenterVertices()
		self.painter.drawPoint(self.origin)
		self.drawTile(self.centerVertices, self.origin, self.renderLayers)

		self.painter.setClipping(False)

		diskCenterX = -1 * self.diskDiameter/2 + self.origin.x()
		diskCenterY = -1 * self.diskDiameter/2 + self.origin.y()
		self.painter.setPen(QPen(QColor(5, 0, 127, 255), 3))
		self.painter.drawEllipse(QRect(diskCenterX, diskCenterY, self.diskDiameter, self.diskDiameter))

		self.painter.end()
		del self.painter
		self.centerVertices = []
		print(self.drawnCount)
		self.drawnCount = 0
		self.drawnTiles = defaultdict(set)
