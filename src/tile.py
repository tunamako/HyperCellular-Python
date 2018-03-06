from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from math_helpers import areCollinear
from reflectionaxis import ArcAxis, LineAxis

class Tile:
	def __init__(self, vertices, center, layer, origin, diskDiameter):

		self.region = None
		self.vertices = vertices
		self.edges = []
		self.neighbors = []
		self.center = center
		self.layer = layer

		for A, B in zip(vertices[-1:] + vertices[:-1], vertices):
			if areCollinear(A, B, origin):
				self.edges.append(LineAxis(A, B))
			else:
				self.edges.append(ArcAxis(A, B, origin, diskDiameter))


		edgeRegions = []
		for edge in self.edges:
			rect = QRect(edge.center.x() - edge.radius, edge.center.y() - edge.radius, edge.radius * 2, edge.radius * 2)
			edgeRegions.append(QRegion(rect, QRegion.Ellipse))

		self.region = QRegion(QRect(origin.x() - diskDiameter/2, origin.y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion.Ellipse)
		
		for region in edgeRegions:
			if region.contains(QPoint(center.x(), center.y())):
				self.region = self.region.intersected(region)
			else:
				self.region = self.region.subtracted(region)


	def draw(self, painter):
		painter.drawPoint(self.center)
		for edge in self.edges:
			edge.draw(painter)