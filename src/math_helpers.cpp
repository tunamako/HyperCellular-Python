#include "math_helpers.h"

#include <QLineF>
#include <QPoint>

#include <math.h>
#include <algorithm>
#include <iostream>

float distance(QPointF *A, QPointF *B){
	return sqrt(pow((B->x() - A->x()), 2) + pow((B->y() - A->y()), 2));
}

QPointF midpoint(QPointF *A, QPointF *B) {
	return QPointF((A->x() + B->x())/2, (A->y() + B->y())/2);
}

bool areCollinear(QPointF *A, QPointF *B, QPointF *C) {
	QLineF AB(*A, *B);
	QLineF BC(*B, *C);
	QLineF AC(*A, *C);
	return ceil(AB.angleTo(BC)) == ceil(AB.angleTo(AC));
}