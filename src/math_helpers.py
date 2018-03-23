from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math

def distance(A, B):
	return math.sqrt(math.pow((B.x() - A.x()), 2) + math.pow((B.y() - A.y()), 2))

def midpoint(A, B):
	return QPointF((A.x() + B.x())/2, (A.y() + B.y())/2)

def slope(A, B):
	return ((B.y() - A.y())/(B.x() - A.x()))

def areCollinear(A, B, C):
	try:
		diff = abs(slope(B,C) - slope(A,B))
	except:
		diff = 1

	return diff <= 0.00000001
