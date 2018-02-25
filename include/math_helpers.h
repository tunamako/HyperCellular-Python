#ifndef HELP_H
#define HELP_H

#include <QPoint>

QPointF midpoint(QPointF a, QPointF b);
double distance(QPointF a, QPointF b);
bool areCollinear(QPointF *a, QPointF *b, QPointF *c);

#endif