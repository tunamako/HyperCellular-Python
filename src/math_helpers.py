from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math

def distance(A, B):
	return math.sqrt(math.pow((B.x() - A.x()), 2) + math.pow((B.y() - A.y()), 2))

def midpoint(A, B):
	return QPointF((A.x() + B.x())/2, (A.y() + B.y())/2)

def areCollinear(A, B, C):
	AB = QLineF(A, B)
	BC = QLineF(B, C)
	AC = QLineF(A, C)
	return math.ceil(AB.angleTo(BC)) == math.ceil(AB.angleTo(AC))
