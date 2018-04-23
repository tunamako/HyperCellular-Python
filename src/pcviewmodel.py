from PyQt5.QtGui import QColor, QRegion, QPainter, QBrush, QPen, QTransform, QPainterPath
from PyQt5.QtCore import QRect, QPointF, QPoint, QLineF, QRectF
from PyQt5.QtWidgets import QWidget

from tile import Tile

import math
from math_helpers import distance, slope
from collections import defaultdict
from pprint import *

class PoincareViewModel(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.centerVertices = []
		self.origin = QPointF()

		self.drawnTiles = defaultdict(defaultdict)
		self.tiles = []
		self.tilesToUpdate = False
		self.sideCount = 5
		self.adjacentCount = 4
		self.renderDepth = 4
		self.fillMode = True


	#Formula to calculate distance from center of disk to any vertex of the
	#initial polygon is from:
	#http://www.malinc.se/math/noneuclidean/poincaretilingen.php
	def getCenterVertices(self):
		p = self.sideCount
		q = self.adjacentCount
		dist = (self.diskDiameter/2) * math.sqrt(math.cos(math.pi * (1/p + 1/q)) / math.cos(math.pi * (1/p - 1/q)))
		alpha = 2*math.pi/p

		centerVertices = []
		for i in range(p):
			x = self.origin.x() + (dist) * math.cos(i * alpha)
			y = self.origin.y() + (dist) * math.sin(i * alpha)

			centerVertices.append(QPointF(x, y))
		return centerVertices
		
	#Since tiles are indexed by their centers (floating point), we need some leeway
	#with how 'close' two points need to be to be considered the same
	def hasBeenDrawn(self, aPoint):
		precision = 1000
		x = round(precision * aPoint.x())/precision
		y = round(precision * aPoint.y())/precision

		try:
			return self.drawnTiles[x][y]
		except:
			return None

	def addDrawnTile(self, aTile):
		precision = 1000
		x = round(precision * aTile.center.x())/precision
		y = round(precision * aTile.center.y())/precision

		self.drawnTiles[x][y] = aTile

	# Breadth-first construction of tiles by reflection about each side, with the 
	# initial tile centered on the origin. This viewmodel is passed to each tile
	# since the disk's origin and diskDiameter are needed to calculate the arcs that 
	# make up the sides of a tile.
	def drawTiling(self):
		self.drawnCount = 0
		self.drawnTiles.clear()
		self.tiles.clear()
		self.centerVertices.clear()

		centerTile = Tile(self.getCenterVertices(), self, self.renderDepth)
		self.addDrawnTile(centerTile)

		queue = [centerTile]
		while queue:
			curTile = queue.pop()
			curTile.draw(self.painter)
			self.tiles.append(curTile)
			if curTile.layer == 1:
				continue

			for edge in curTile.edges:
				#First reflect the center of the current tile to check if the reflected
				#tile has been drawn before
				reflectedCenter = edge.reflectPoint(curTile.center)
				neighbor = self.hasBeenDrawn(reflectedCenter)

				if neighbor is None:
					#draw and log the new tile
					reflectedVertices = edge.reflectTile(curTile)
					neighbor = Tile(reflectedVertices, self, curTile.layer-1, reflectedCenter)
					queue.insert(0, neighbor)
					self.addDrawnTile(neighbor)

				#construct the list of neighbors
				if neighbor not in curTile.neighbors:
					curTile.neighbors.append(neighbor)
				if curTile not in neighbor.neighbors:
					neighbor.neighbors.append(curTile)

	def paintEvent(self, anEvent):
		self.painter = QPainter(self)
		self.painter.setRenderHint(QPainter.Antialiasing, on=True)

		self.diskDiameter = min(self.size().width(), self.size().height()) - 10
		self.origin.setX(self.size().width()/2)
		self.origin.setY(self.size().height()/2)

		self.painter.setPen(QPen(QColor(122, 0, 127, 255), 3))
		radius = self.diskDiameter/2
		x = self.origin.x()
		y = self.origin.y()
		diskRect = QRect(x - radius, y - radius, self.diskDiameter, self.diskDiameter)
		self.diskRegion = QRegion(diskRect, QRegion.Ellipse)
		self.painter.setClipRegion(self.diskRegion)
		
		if self.tilesToUpdate:
			for tile in self.tiles:
				tile.update(self.painter)
			self.tilesToUpdate = False
		else:
			self.drawTiling()
		
		self.painter.setClipping(False)

		self.painter.setPen(QPen(QColor(5, 0, 127, 255), 3))
		self.painter.drawEllipse(diskRect)
		self.painter.drawPoint(self.origin)
		
		self.painter.end()

	def updateTiles(self):
		self.tilesToUpdate = True
		self.update()

	def areHyperbolicDims(self, p, q):
		 return (p-2)*(q-2) > 4

	def setSideCount(self, count):
		if self.areHyperbolicDims(count, self.adjacentCount):
			self.sideCount = count
			self.update()
			return 0

		return -1

	def setAdjCount(self, count):
		if self.areHyperbolicDims(self.sideCount, count):
			self.adjacentCount = count
			self.update()
			return 0
			
		return -1

	def setRenderDepth(self, depth):
		self.renderDepth = depth
		self.update()

	def mousePressEvent(self, e):
		if self.diskRegion.contains(QPoint(e.x(), e.y())):
			self.parent.controller.clicked(e)

	def toggleFillMode(self):
		self.fillMode = not self.fillMode
		self.update()