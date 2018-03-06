from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math

def distance(A, B):
	return math.sqrt(math.pow((B.x() - A.x()), 2) + math.pow((B.y() - A.y()), 2))

def midpoint(A, B):
	return QPointF((A.x() + B.x())/2, (A.y() + B.y())/2)

def areCollinear(A, B, C):
	if B.x() - A.x() == 0:
		B, C = C, B
	elif C.x() - B.x() == 0:
		A, B = B, A
	mAB = (B.y() - A.y())/(B.x() - A.x())
	mBC = (C.y() - B.y())/(C.x() - B.x())

	return abs(mBC - mAB)<= 0.00001
