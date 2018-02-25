#ifndef HELP_H
#define HELP_H

#include <QPoint>

QPointF midpoint(QPointF *A, QPointF *B);
double distance(QPointF *A, QPointF *B);
bool areCollinear(QPointF *A, QPointF *B, QPointF *C);

#endif