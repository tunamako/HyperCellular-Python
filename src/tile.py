from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from math_helpers import areCollinear
from edge import ArcEdge, LineEdge
import random


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
				self.edges.append(LineEdge(A, B))
			else:
				self.edges.append(ArcEdge(A, B, origin, diskDiameter))
		"""
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
		"""

	def draw(self, painter):
		"""
		#Fill tile
		colors = [
			QColor(255, 140, 0, 255), 	#orange
			QColor(65,105,225, 255),	#blue
			#QColor(0, 0, 0, 255),		#black
		]
		path = QPainterPath()
		path.addRegion(self.region)
		painter.fillPath(path, QBrush(QColor(random.choice(colors))))
		"""
		#Draw Border
		painter.setPen(QPen(QColor(0,0,255,255), 2))
		#painter.drawPoint(self.center)
		for edge in self.edges:
			edge.draw(painter)