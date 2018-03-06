#ifndef REFLECTIONAXIS_H
#define REFLECTIONAXIS_H

#include <QWidget>
#include <QPainter>
#include <QPoint>
#include <QVector>

class ReflectionAxis {

public:
	ReflectionAxis();
	virtual ~ReflectionAxis();

	virtual QPointF *reflectPoint(QPointF *aPoint);
	QVector<QPointF *> *reflectPoints(QVector<QPointF *> *aPoint);
	virtual void draw(QPainter *painter);
};

class LineAxis : public ReflectionAxis {

public:
	LineAxis(QPointF *A, QPointF *B);
	virtual ~LineAxis();

	virtual QPointF *reflectPoint(QPointF *aPoint);
	virtual void draw(QPainter *painter);


protected:
	QPointF *A;
	QPointF *B;
	float y_intercept;
	float slope;
};

class ArcAxis : public ReflectionAxis {

public:
	ArcAxis(QPointF *A, QPointF *B, QPointF *origin, int diskDiameter);
	virtual ~ArcAxis();

	virtual QPointF *reflectPoint(QPointF *aPoint);
	virtual void draw(QPainter *painter);

protected:
	QPointF *A;
	QPointF *B;
	QPointF *center;
	float radius;
};

#endif