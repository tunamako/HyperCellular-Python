#include "reflectionaxis.h"

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>
#include <unordered_set>
#include <tuple>

ReflectionAxis::ReflectionAxis() {}
ReflectionAxis::~ReflectionAxis() {}
QPointF *ReflectionAxis::reflectPoint(QPointF *aPoint) {}
QVector<QPointF *> *ReflectionAxis::reflectPoints(QVector<QPointF *> *aPoint) {}
void ReflectionAxis::draw(QPainter *painter) {}

LineAxis::LineAxis(QPointF *A, QPointF *B) {
	this->A = A;
	this->B = B;
}
LineAxis::~LineAxis() {}

QPointF *LineAxis::reflectPoint(QPointF *aPoint) {
	double x = A->x();
	double y = A->y();
	double m = slope;
	double b = y_intercept;

	double d = (x + (y - b)*m)/(1 + pow(m, 2));

	return new QPointF(2*d - x, 2*d*m - y + 2*b);
}

QVector<QPointF *> *LineAxis::reflectPoints(QVector<QPointF *> *vertices) {
}

void LineAxis::draw(QPainter *painter) {
	painter->drawLine(*this->A, *this->B);
}




ArcAxis::ArcAxis(QPointF *A, QPointF *B, QPointF *origin, double diskDiameter) {
	/*
	this->A = A;
	this->B = B;

	this->center = origin;
	this->radius = diskDiameter/2;
	QPointF c = *this->reflectPoint(&a);

	a.setX(a.x()-c.x());
	a.setY(a.y()-c.y());
	b.setX(b.x()-c.x());
	b.setY(b.y()-c.y());

	double Z1 = a.x() * a.x() + a.y() * a.y();
	double Z2 = b.x() * b.x() + b.y() * b.y();
	double D = 2 * (a.x() * b.y() - b.x() * a.y());

	double centerX = (Z1 * b.y() - Z2 * a.y()) / D + c.x();
	double centerY = (a.x() * Z2 - b.x() * Z1) / D + c.y();

	circle_t circ;
	circ.center = new QPointF(centerX, centerY);
	circ.radius = distance(*circ.center, c);

	return circ;
	*/
}
ArcAxis::~ArcAxis() {}

QPointF *ArcAxis::reflectPoint(QPointF *aPoint) {
	//std::cout << aCircle.center->x() << ", " << aCircle.center->y() << std::endl;
	double x = aPoint->x();
	double y = aPoint->y();
	double x0 = center->x();
	double y0 = center->y();
	double invX = x0 + (pow(radius, 2) * (x-x0)) / (pow(x-x0, 2) + pow(y-y0, 2));
	double invY = y0 + (pow(radius, 2) * (y-y0)) / (pow(x-x0, 2) + pow(y-y0, 2));

	return new QPointF(invX, invY);
}

QVector<QPointF *> *ArcAxis::reflectPoints(QVector<QPointF *> *vertices) {
}

void ArcAxis::draw(QPainter *painter) {
	//rectangle inscribed by aCircle
	QRectF rect(center->x() - radius, center->y() - radius, radius * 2, radius * 2);
	QLineF lineA(*center, *A);
	QLineF lineB(*center, *B);

	double sweepAngle = lineA.angleTo(lineB);
	if(sweepAngle > 180)
		sweepAngle -= 360;

	painter->drawArc(rect, 16 * lineA.angle(), 16 * sweepAngle);
}
