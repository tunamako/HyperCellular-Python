from PyQt5.QtGui import QColor, QRegion, QPainterPath, QBrush
from PyQt5.QtCore import QRect, QPoint

from math_helpers import areCollinear
from edge import ArcEdge, LineEdge
import random


class Tile:
	def __init__(self, vertices, center, layer, origin, diskDiameter):

		self.edges = []
		self.neighbors = []
		self.center = center
		self.layer = layer
		self.vertices = vertices
		self.color = QColor(255, 255, 255, 255)
		self.nextColor = None

		self.region = QRegion(QRect(origin.x() - diskDiameter/2, origin.y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion.Ellipse)

		for A, B in zip(vertices[-1:] + vertices[:-1], vertices):
			if areCollinear(A, B, origin):
				edge = LineEdge(A, B)
				region = edge.getRegion(center, origin, diskDiameter)
			else:
				edge = ArcEdge(A, B, origin, diskDiameter)
				region = edge.getRegion()

			self.edges.append(edge)
			
			if region.contains(QPoint(center.x(), center.y())):
				self.region = self.region.intersected(region)
			else:
				self.region = self.region.subtracted(region)
			
		
	def draw(self, painter):
		path = QPainterPath()
		path.addRegion(self.region)
		painter.fillPath(path, QBrush(self.color))

		for edge in self.edges:
			edge.draw(painter)
