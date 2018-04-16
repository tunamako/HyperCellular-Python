from PyQt5.QtGui import QRegion, QPolygon, QPen, QColor
from PyQt5.QtCore import QRect, QRectF, QPoint, QPointF, QLineF

from math_helpers import distance, slope, midpoint
import math

class Edge:
	def __init__(self):
		pass		
	def reflectPoint(self, aPoint):
		pass
	def reflectTile(self, aTile):
		return [self.reflectPoint(p) for p in aTile.vertices]
	def draw(self, painter):
		pass
 
class LineEdge(Edge):
	def __init__(self, A, B):
		super().__init__()
		self.A = QPointF(A.x(), A.y())
		self.B = QPointF(B.x(), B.y())

		try:
			self.slope = slope(A, B)
		except ZeroDivisionError as e:
			self.slope = None
			self.y_intercept = None
			return

		self.y_intercept = (A.y() - (self.slope * A.x()))

	def reflectPoint(self, aPoint):
		m = self.slope
		b = self.y_intercept
		x = aPoint.x()
		y = aPoint.y()

		if m == None:
			#axis of reflection is vertical
			invX = x - 2 * (x - self.A.x())
			invY = y
		elif -0.001 <= m <= 0.001:
			#axis of reflection is horizontal
			invX = x
			invY = y - 2 * (y - self.A.y())
		else:
			intersectX = (x + m*(y-b))/(m**2 + 1)
			intersectY = -1/m*intersectX + y + x/m
			invX = x + 2*(intersectX - x)
			invY = y + 2*(intersectY - y)
		return QPointF(invX, invY)
		
	def draw(self, painter):
		painter.drawLine(self.A, self.B)
		#painter.drawPolygon(self.trianglePoly)

	def getExtendedX(self, d, m):
		#returns the x-distance needed to extend a point d-distance along this line
		return math.sqrt((d*d) / (1 + 1 * m**2))

	def getRegion(self, polygonCenter, origin, radius):
		#create a triangle that contains the entire tile using three points:
		
		#point on edge of disk where this lineedge would intersect if extended
		#get intersections of this lineedge with circle and pick the one closer to the polygon center
		m = self.slope
		b = self.y_intercept
		
		if m == None:
			#line is vertical
			if polygonCenter.y() > origin.y():
				diskPoint = QPoint(origin.x(), origin.y() + radius)
			else:
				diskPoint = QPoint(origin.x(), origin.y() - radius)
		elif -0.001 <= m <= 0.001:
			#line is horizontal
			if polygonCenter.x() > origin.x():
				diskPoint = QPoint(origin.x() + radius, origin.y())
			else:
				diskPoint = QPoint(origin.x() - radius, origin.y())
		else:
			deltaX = self.getExtendedX(radius, self.slope)

			diskPointX_A = origin.x() + deltaX
			diskPointY_A = m * diskPointX_A + b
			diskPointX_B = origin.x() - deltaX
			diskPointY_B = m * diskPointX_B + b

			candidateA = QPoint(diskPointX_A, diskPointY_A)
			candidateB = QPoint(diskPointX_B, diskPointY_B)

			if distance(polygonCenter, candidateA) < distance(polygonCenter, candidateB):
				diskPoint = candidateA
			else:
				diskPoint = candidateB

		#point on edge of disk where the line orthogonal to this lineedge would intersect
		orthoDiskPoint = QPoint()
		edgeMidpoint = midpoint(self.A, self.B)

		if m == None:
			#line is vertical
			if polygonCenter.x() < edgeMidpoint.x():
				orthoDiskPoint = QPoint(edgeMidpoint.x() + radius, edgeMidpoint.y())
			else:
				orthoDiskPoint = QPoint(edgeMidpoint.x() - radius, edgeMidpoint.y())
		elif -0.001 <= m <= 0.001:
			#line is horizontal
			if polygonCenter.y() < edgeMidpoint.y():
				orthoDiskPoint = QPoint(edgeMidpoint.x(), edgeMidpoint.y() + radius)
			else:
				orthoDiskPoint = QPoint(edgeMidpoint.x(), edgeMidpoint.y() - radius)
		else:
			deltaX = self.getExtendedX(radius, -1/self.slope)

			orthoDiskPointX_A = origin.x() + deltaX
			orthoDiskPointY_A = m * orthoDiskPointX_A + b
			orthoDiskPointX_B = origin.x() - deltaX
			orthoDiskPointY_B = m * orthoDiskPointX_B + b

			candidateA = QPoint(orthoDiskPointX_A, orthoDiskPointY_A)
			candidateB = QPoint(orthoDiskPointX_B, orthoDiskPointY_B)

			if distance(polygonCenter, candidateA) >distance(polygonCenter, candidateB):
				orthoDiskPoint = candidateA
			else:
				orthoDiskPoint = candidateB			


		self.tripoints = [QPoint(origin.x(), origin.y()), diskPoint, orthoDiskPoint]
		self.trianglePoly = QPolygon([QPoint(origin.x(), origin.y()), diskPoint, orthoDiskPoint])

		return QRegion(self.trianglePoly)

class ArcEdge(Edge):
	def __init__(self, A, B, origin, diskDiameter):
		super().__init__()
		self.A = QPointF(A.x(), A.y())
		self.B = QPointF(B.x(), B.y())
		A = QPointF(A.x(), A.y())
		B = QPointF(B.x(), B.y())

		self.center = origin
		self.radius = diskDiameter/2
		C = self.reflectPoint(A)

		#Check if given points form a vertical segment: if so, rearrange points
		if B.x() - A.x() == 0:
			B, C = C, B
		elif C.x() - B.x() == 0:
			A, B = B, A

		try:
			mA = slope(A, B)
			mB = slope(B, C)
		except:
			return
			
		#Use the intersection of the perpendicular bisectors of AB and BC as the center of the circle
		centerX = (mA*mB*(A.y()-C.y()) + mB*(A.x()+B.x()) - mA*(B.x() + C.x())) / (2*(mB - mA))
		try:
			centerY = (-1/mA)*(centerX - (A.x() + B.x())/2) + (A.y() + B.y())/2
		except:
			centerY = (-1/mB)*(centerX - (B.x() + C.x())/2) + (B.y() + C.y())/2

		self.center = QPointF(centerX, centerY)
		self.radius = distance(self.center, A)
		self.collinear = False

	def reflectPoint(self, aPoint):
		x = aPoint.x()
		y = aPoint.y()
		x0 = self.center.x()
		y0 = self.center.y()
		invX = x0 + (self.radius**2 * (x-x0)) / ((x-x0)**2 + (y-y0)**2)
		invY = y0 + (self.radius**2 * (y-y0)) / ((x-x0)**2 + (y-y0)**2)

		return QPointF(invX, invY)

	def draw(self, painter):
		rect = QRectF(self.center.x() - self.radius, self.center.y() - self.radius, self.radius * 2, self.radius * 2)
		lineA = QLineF(self.center, self.A)
		lineB = QLineF(self.center, self.B)

		sweepAngle = lineA.angleTo(lineB)
		if(sweepAngle > 180):
			sweepAngle -= 360
		
		painter.drawArc(rect, 16 * lineA.angle(), 16 * sweepAngle)

	def getRegion(self, polygonCenter, origin, radius):
		rect = QRect(self.center.x() - self.radius, self.center.y() - self.radius, self.radius * 2, self.radius * 2)
		return QRegion(rect, QRegion.Ellipse)