#include "math_helpers.h"

#include <QLine>
#include <QPoint>

#include <math.h>
#include <algorithm>

double distance(QPointF a, QPointF b){
	return sqrt(pow((b.x() - a.x()), 2) + pow((b.y() - a.y()), 2));
}

QPointF midpoint(QPointF a, QPointF b) {
	return QPointF((a.x() + b.x())/2, (a.y() + b.y())/2);
}

bool areCollinear(QPointF *a, QPointF *b, QPointF *c) {
	QLineF AB(*a, *b);
	QLineF BC(*b, *c);
	QLineF AC(*a, *c);
	return ceil(AB.angleTo(BC)) == ceil(AB.angleTo(AC));
}