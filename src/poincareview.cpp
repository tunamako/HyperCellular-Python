#include "poincareview.h"
#include "reflectionaxis.h"
#include "math_helpers.h"

#include <QWidget>
#include <QPainter>
#include <QPainterPath>
#include <QVector>
#include <QBrush>
#include <QRegion>
#include <QString>
#include <QOpenGLFunctions>

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>
#include <unordered_set>

PoincareView::PoincareView(QWidget *parent) :
	QOpenGLWidget(parent) {

	this->drawnCount = 0;
	this->drawnTiles = std::map<double, std::unordered_set<double> >();
	this->sideCount = 7;
	this->adjacentCount = 3;
	this->renderLayers = 3;
}
PoincareView::~PoincareView(){}

QVector<QPointF *> *PoincareView::getCenterVertices() {
	QVector<QPointF *> *vertices = new QVector<QPointF *>();
	int p = sideCount;
	int q = adjacentCount;
	//Put this line in its own method
	double dist = (diskDiameter/2) * sqrt(cos(M_PI/p + M_PI/q)*cos(M_PI/q) / (sin(2*M_PI/q) * sin(M_PI/p) + cos(M_PI/p + M_PI/q)* cos(M_PI/q)));
	double alpha = 2 * M_PI / sideCount;

	for(int i = 0; i < sideCount; i++) {
		double x = origin->x() + (dist) * cos(i * alpha);
		double y = origin->y() + (dist) * sin(i * alpha);

		vertices->push_back(new QPointF(x, y));
	}
	return vertices;
}

bool PoincareView::hasBeenDrawn(QPointF *aPoint) {
	int precision = pow(10,precision);
	double x = round(precision * aPoint->x())/precision;
	double y = round(precision * aPoint->y())/precision;

	if(drawnTiles.count(x) == 1) {
		if(drawnTiles[x].count(y) == 1)
			return true;
	} else {
		drawnTiles[x] = std::unordered_set<double>();
	}

	drawnTiles[x].insert(y);
	return false;
}

void PoincareView::drawTile(QVector<QPointF *> *vertices, QPointF *center, int layers) {
	QVector<QPointF *> *reflectedVertices = new QVector<QPointF *>(sideCount);
	QPointF *reflectedCenter;
	ReflectionAxis *axis;

	if(hasBeenDrawn(center))
		return;

	drawnCount++;
	painter->drawPoint(*center);

	//Draw and reflect across each side of this tile
	for(auto it = vertices->begin(); it != vertices->end(); ++it) {
		QPointF *A = *it;
		QPointF *B = (it + 1 != vertices->end())
			? *(it + 1)
			: *(vertices->begin());
	
		if(areCollinear(A, B, origin))
			axis = new LineAxis(A, B);
		else
			axis = new ArcAxis(A, B, origin, diskDiameter);

		axis->draw(painter);
		if(layers == 1)
			continue;

		reflectedCenter = axis->reflectPoint(center);
		reflectedVertices->clear();

		for(auto j : *vertices) {
			reflectedVertices->push_back(axis->reflectPoint(j));
		}

		drawTile(reflectedVertices, reflectedCenter, layers - 1);
	}
}

void PoincareView::paintEvent(QPaintEvent *e) {
	diskDiameter = std::min(size().width(), size().height()) - 10;
	painter = new QPainter(this);
	painter->setRenderHint(QPainter::HighQualityAntialiasing);
	diskPath = new QPainterPath();

	origin = new QPointF(size().width()/2, size().height()/2 );

	QVector<QPointF *> *centerVertices = getCenterVertices();
	painter->setPen(QPen(QColor(122, 0, 127, 255), 2));
	diskRegion = new QRegion(QRect(origin->x() - diskDiameter/2, origin->y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion::Ellipse);
	diskPath->addRegion(*diskRegion);
	painter->setClipRegion(*diskRegion);

	drawTile(centerVertices, origin, renderLayers);

	painter->setClipping(false);
	int diskCenterX = -diskDiameter/2 + origin->x();
	int diskCenterY = -diskDiameter/2 + origin->y();
	painter->setPen(QPen(QColor(5, 0, 127, 255), 3));
	painter->drawEllipse(QRect(diskCenterX, diskCenterY, diskDiameter, diskDiameter));

	painter->end();
	std::cout << drawnCount << std::endl;
	drawnCount = 0;
	drawnTiles.clear();
}
