#include "reflectionaxis.h"
#include "math_helpers.h"

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>
#include <unordered_set>
#include <tuple>

ReflectionAxis::ReflectionAxis() {}
ReflectionAxis::~ReflectionAxis() {}
QPointF *ReflectionAxis::reflectPoint(QPointF *aPoint) {}
void ReflectionAxis::draw(QPainter *painter) {}


LineAxis::LineAxis(QPointF *A, QPointF *B) {
	this->A = new QPointF(A->x(), A->y());
	this->B = new QPointF(B->x(), B->y());

	this->slope = (B->y() - A->y())/(B->x() - A->x());
	this->y_intercept = A->y() - (this->slope * A->x());
}
LineAxis::~LineAxis() {}

QPointF *LineAxis::reflectPoint(QPointF *aPoint) {
	float denom = 1 + pow(A->x(), 2);
	float m = this->slope;
	float b = this->y_intercept;
	float x = aPoint->x();
	float y = aPoint->y();

	float invX = ((1 - x*pow(m,2)) + 2*m*y - 2*m*b) / denom;
	float invY = (2*m*x - (1 - x*pow(m,2))*y + 2*b) / denom;

	return new QPointF(invX, invY);
}

void LineAxis::draw(QPainter *painter) {
	painter->drawLine(*A, *B);
}


ArcAxis::ArcAxis(QPointF *A, QPointF *B, QPointF *origin, int diskDiameter) {
	this->A = new QPointF(A->x(), A->y());
	this->B = new QPointF(B->x(), B->y());
	QPointF *tempA = new QPointF(A->x(), A->y());
	QPointF *tempB = new QPointF(B->x(), B->y());

	this->center = origin;

	this->radius = diskDiameter/2;
	QPointF *C = this->reflectPoint(A);

	tempA->setX(tempA->x() - C->x());
	tempA->setY(tempA->y() - C->y());
	tempB->setX(tempB->x() - C->x());
	tempB->setY(tempB->y() - C->y());

	float Z1 = tempA->x() * tempA->x() + tempA->y() * tempA->y();
	float Z2 = tempB->x() * tempB->x() + tempB->y() * tempB->y();
	float D = 2 * (tempA->x() * tempB->y() - tempB->x() * tempA->y());

	this->center = new QPointF();
	this->center->setX((Z1 * tempB->y() - Z2 * tempA->y()) / D + C->x());
	this->center->setY( (tempA->x() * Z2 - tempB->x() * Z1) / D + C->y() );

	this->radius = distance(this->center, C);
}
ArcAxis::~ArcAxis() {}

QPointF *ArcAxis::reflectPoint(QPointF *aPoint) {
	float x = aPoint->x();
	float y = aPoint->y();
	float x0 = center->x();
	float y0 = center->y();
	float invX = x0 + (pow(radius, 2) * (x-x0)) / (pow(x-x0, 2) + pow(y-y0, 2));
	float invY = y0 + (pow(radius, 2) * (y-y0)) / (pow(x-x0, 2) + pow(y-y0, 2));

	return new QPointF(invX, invY);
}

void ArcAxis::draw(QPainter *painter) {
	//rectangle inscribed by aCircle
	QRectF rect(center->x() - radius, center->y() - radius, radius * 2, radius * 2);
	QLineF lineA(*center, *A);
	QLineF lineB(*center, *B);

	float sweepAngle = lineA.angleTo(lineB);
	if(sweepAngle > 180)
		sweepAngle -= 360;
	
	painter->drawArc(rect, 16 * lineA.angle(), 16 * sweepAngle);
	
}
