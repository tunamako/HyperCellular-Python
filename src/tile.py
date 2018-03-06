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

	def draw(self, painter):
		painter.drawPoint(self.center)
		for edge in self.edges:
			edge.draw(painter)