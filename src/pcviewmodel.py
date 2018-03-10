from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tile import Tile

import math
from collections import defaultdict
from pprint import *

class PoincareViewModel(QOpenGLWidget):
	def __init__(self):
		super().__init__()
		self.centerVertices = []
		self.origin = QPointF()

		self.drawnTiles = defaultdict(set)

		self.tiles = []
		self.sideCount = 5
		self.adjacentCount = 4
		self.renderDepth = 5

	def getCenterVertices(self):
		p = self.sideCount
		q = self.adjacentCount
		dist = (self.diskDiameter/2) * math.sqrt(math.cos(math.pi/p + math.pi/q)*math.cos(math.pi/q) / (math.sin(2*math.pi/q) * math.sin(math.pi/p) + math.cos(math.pi/p + math.pi/q)* math.cos(math.pi/q)))
		alpha = 2*math.pi/p

		centerVertices = []
		for i in range(p):
			x = self.origin.x() + (dist) * math.cos(i * alpha)
			y = self.origin.y() + (dist) * math.sin(i * alpha)

			centerVertices.append(QPointF(x, y))
		return centerVertices
		
	def hasBeenDrawn(self, aPoint):
		precision = 1000
		x = round(precision * aPoint.x())/precision
		y = round(precision * aPoint.y())/precision

		if x in self.drawnTiles and y in self.drawnTiles[x]:
			return True

		self.drawnTiles[x].add(y)
		return False

	# Breadth-first construction of tiles by reflection about each side, with the 
	# initial tile centered on the origin. The disk origin and diskDiameter are 
	# passed to each tile since they are needed to calculate the arcs that 
	# make up the sides of a tile.
	def drawTiling(self):
		queue = [Tile(self.getCenterVertices(), self.origin, self.renderDepth, self.origin, self.diskDiameter)]

		while queue:
			curTile = queue.pop()
			curTile.draw(self.painter)
			self.tiles.append(curTile)

			if curTile.layer == 1:
				continue

			for edge in curTile.edges:
				reflectedCenter = edge.reflectPoint(curTile.center)
				if self.hasBeenDrawn(reflectedCenter):
					continue

				reflectedVertices = edge.reflectPoints(curTile.vertices)

				neighbor = Tile(reflectedVertices, reflectedCenter, curTile.layer-1, self.origin, self.diskDiameter)
				curTile.neighbors.append(neighbor)
				queue.insert(0, neighbor)
		
	def paintEvent(self, QPaintEvent):
		self.drawnCount = 0
		self.drawnTiles.clear()
		self.tiles.clear()

		self.diskDiameter = min(self.size().width(), self.size().height()) - 10
		self.origin.setX(self.size().width()/2)
		self.origin.setY(self.size().height()/2)

		self.painter = QPainter(self)
		self.painter.eraseRect(0, 0, self.size().width(), self.size().height())
		self.painter.setPen(QPen(QColor(122, 0, 127, 255), 2))

		radius = self.diskDiameter/2
		x = self.origin.x()
		y = self.origin.y()
		diskRect = QRect(x - radius, y - radius, self.diskDiameter, self.diskDiameter)
		self.painter.setClipRegion(QRegion(diskRect, QRegion.Ellipse))

		self.drawTiling()

		self.painter.setClipping(False)
		self.painter.setPen(QPen(QColor(5, 0, 127, 255), 3))
		self.painter.drawEllipse(diskRect)

		self.centerVertices = []
		self.painter.end()
		del self.painter

	def updateTiles(self, aTileList):
		pass

	def setStateList(self, aStateList):
		pass

	def setStateColor(self, aState, aColor):
		pass

	def areValidDims(self, p, q):
		 return (p-2)*(q-2) > 4

	def setSideCount(self, count):
		if self.areValidDims(count, self.adjacentCount):
			self.sideCount = count
			self.update()
			return 0

		return -1

	def setAdjCount(self, count):
		if self.areValidDims(count, self.sideCount):
			self.adjacentCount = count
			self.update()
			return 0
			
		return -1

	def setRenderDepth(self, depth):
		self.renderDepth = depth
		self.update()
