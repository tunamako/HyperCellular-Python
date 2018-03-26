from PyQt5.QtGui import QColor, QRegion, QPainter, QBrush, QPen
from PyQt5.QtCore import QRect, QPointF
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

		self.drawnTiles = defaultdict(set)
		self.tiles = []
		self.toBeUpdated = []
		self.sideCount = 5
		self.adjacentCount = 4
		self.renderDepth = 5


	#Formula to calculate distance from center of disk to any vertex of the
	#initial polygon is from:
	#http://www.malinc.se/math/noneuclidean/poincaretilingen.php
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
		self.drawnCount = 0
		self.drawnTiles.clear()
		self.tiles.clear()
		self.centerVertices.clear()

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

				reflectedVertices = edge.reflectTile(curTile)

				neighbor = Tile(reflectedVertices, reflectedCenter, curTile.layer-1, self.origin, self.diskDiameter)
				curTile.neighbors.append(neighbor)
				queue.insert(0, neighbor)

	def updateTiles(self):
		for tile in self.toBeUpdated:
			tile.color = tile.nextColor
			tile.nextColor = None
			tile.draw(self.painter)
		self.toBeUpdated.clear()

	def getExtendedX(self, d, m):
		return math.sqrt((d*d) / (1 + 1 * m*m))

	def drawTestRect(self):
		A = QPointF(self.origin.x()*(.8), self.origin.y()*(.8))
		B = QPointF(self.origin.x()*(.7), self.origin.y()*(.7))
		polyCenter = QPoint(self.origin.x()*(.7), self.origin.y()*(.6))

		initLine = QLineF(A, B)
		azimuth = QLineF(A, QPointF(A.x(), B.y())).angleTo(QLineF(A,B))
		mAB = slope(A, B)
		b = A.y() - mAB * A.x()

		segMidx = self.getExtendedX(self.diskDiameter/4, mAB)
		if B.x() < self.origin.x():
			segMidx *= -1
		segMidx += self.origin.x()

		segMidy = mAB * segMidx + b

		segMid = QPointF(segMidx, segMidy)
		self.painter.drawPoint(segMid)
		self.painter.drawPoint(A)
		self.painter.drawPoint(B)
		self.painter.drawPoint(polyCenter)

		delta = self.getExtendedX(self.diskDiameter/4, -1/mAB)

		rectCenterx = segMid.x() - delta
		rectCenterOne = QPointF(rectCenterx, (-1/mAB) * rectCenterx + (2*segMid.x() - b))
		rectCenterx = segMid.x() + delta
		rectCenterTwo = QPointF(rectCenterx, (-1/mAB) * rectCenterx + (2*segMid.x() - b))

		if distance(polyCenter, rectCenterOne) < distance(polyCenter, rectCenterTwo):
			self.painter.drawPoint(rectCenterOne)
		else:
			self.painter.drawPoint(rectCenterTwo)

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
		self.painter.setClipRegion(QRegion(diskRect, QRegion.Ellipse))
		
		if self.toBeUpdated:
			self.updateTiles()
		else:
			self.painter.eraseRect(0, 0, self.size().width(), self.size().height())
			self.drawTiling()
		

		#self.drawTestRect()
		self.painter.setClipping(False)
		self.painter.setPen(QPen(QColor(5, 0, 127, 255), 3))
		self.painter.drawEllipse(diskRect)
		self.painter.drawPoint(self.origin)
		
		self.painter.end()

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
		if self.areValidDims(self.sideCount, count):
			self.adjacentCount = count
			self.update()
			return 0
			
		return -1

	def setRenderDepth(self, depth):
		self.renderDepth = depth
		self.update()
