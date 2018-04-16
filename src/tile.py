from PyQt5.QtGui import QColor, QRegion, QPainterPath, QBrush, QPolygon
from PyQt5.QtCore import QRect, QPoint

from math_helpers import areCollinear
from edge import ArcEdge, LineEdge
import random


class Tile:
	def __init__(self, vertices, model, layer, center=None):

		self.edges = []
		self.neighbors = []
		self.center = center if center else model.origin
		self.layer = layer
		self.vertices = vertices
		self.color = QColor(0,0, 0, 255)
		self.nextColor = None
		self.fillMode = model.fillMode
		self.region = model.diskRegion

		origin = model.origin
		diskDiameter = model.diskDiameter
		for A, B in zip(vertices[-1:] + vertices[:-1], vertices):
			if areCollinear(A, B, origin):
				edge = LineEdge(A, B)
				self.edges.append(edge)
			else:
				edge = ArcEdge(A, B, origin, diskDiameter)
				self.edges.insert(0, edge)

		if self.fillMode:
			for edge in self.edges:
				region = edge.getRegion(self.center, origin, diskDiameter/2)

				if model.fillMode and region.contains(QPoint(self.center.x(), self.center.y())):
					self.region = self.region.intersected(region)
				else:
					self.region = self.region.subtracted(region)
			
	def draw(self, painter):
		if self.fillMode:
			path = QPainterPath()
			path.addRegion(self.region)
			painter.fillPath(path, QBrush(self.color))

		for edge in self.edges:
			edge.draw(painter)

	def update(self, painter):
		if self.nextColor:
			self.color = self.nextColor
			self.nextColor = None
		self.draw(painter)
