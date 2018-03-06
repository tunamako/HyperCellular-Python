from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tile import Tile

import math
import random
from collections import defaultdict
from pprint import *

class PoincareView(QOpenGLWidget):
	def __init__(self):
		super().__init__()
		self.centerVertices = []
		self.origin = QPointF()

		self.drawnCount = 0
		self.drawnTiles = defaultdict(set)
		self.tiles = []
		self.sideCount = 5
		self.adjacentCount = 4
		self.renderLayers = 5

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

	def drawTiling(self, vertices, center, layers):
		queue = [Tile(vertices, center, layers, self.origin, self.diskDiameter)]

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
		self.drawTiling(self.centerVertices, self.origin, self.renderLayers)

		self.painter.setClipping(False)

		diskCenterX = -1 * self.diskDiameter/2 + self.origin.x()
		diskCenterY = -1 * self.diskDiameter/2 + self.origin.y()
		self.painter.setPen(QPen(QColor(5, 0, 127, 255), 3))
		self.painter.drawEllipse(QRect(diskCenterX, diskCenterY, self.diskDiameter, self.diskDiameter))


		for tile in self.tiles:
			path = QPainterPath()
			path.addRegion(tile.region)
			self.painter.fillPath(path, QBrush(QColor(random.random() * 255, random.random() * 255, random.random() * 255, 255)))
			self.painter.fillPath(path, QBrush(QColor(random.random() * 255, random.random() * 255, random.random() * 255, 255)))



		self.painter.end()
		del self.painter
		self.centerVertices = []
		self.drawnCount = 0
		self.drawnTiles.clear()
		self.tiles.clear()
