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
	def getRegion(self, polygonCenter, origin, radius):
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

	def getRegion(self, polygonCenter, origin, radius):
		#create a triangle that contains the entire tile using three points:
		#	origin of the disk
		#	point on edge of disk where this lineedge would intersect if extended
		#	point on edge of disk where the line orthogonal to this edge would intersect
		
		theta = math.atan2(self.A.y() - origin.y(), self.A.x() - origin.x())

		diskPointX = origin.x() + math.cos(theta) * radius
		diskPointY = origin.y() + math.sin(theta) * radius

		diskPoint = QPoint(diskPointX, diskPointY)

		#determine which side of the edge the polygon is on
		if math.atan2(polygonCenter.y() - origin.y(), polygonCenter.x() - origin.x()) < theta:
			gamma = theta - math.pi/3
		else:
			gamma = theta + math.pi/3

		orthoDiskPointX = origin.x() + math.cos(gamma) * radius
		orthoDiskPointY = origin.y() + math.sin(gamma) * radius

		orthoDiskPoint = QPoint(orthoDiskPointX, orthoDiskPointY)

		self.trianglePoly = QPolygon([origin.toPoint(), diskPoint, orthoDiskPoint])
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