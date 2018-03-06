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

	this->centerVertices = new QVector<QPointF *>();
	this->origin = new QPointF();

	this->drawnCount = 0;
	this->drawnTiles = std::map<float, std::unordered_set<float> >();
	this->sideCount = 7;
	this->adjacentCount = 3;
	this->renderLayers = 6;
}
PoincareView::~PoincareView(){}

void PoincareView::genCenterVertices() {
	int p = sideCount;
	int q = adjacentCount;
	//Put this line in its own method
	float dist = (diskDiameter/2) * sqrt(cos(M_PI/p + M_PI/q)*cos(M_PI/q) / (sin(2*M_PI/q) * sin(M_PI/p) + cos(M_PI/p + M_PI/q)* cos(M_PI/q)));
	float alpha = 2 * M_PI / sideCount;

	for(u_int i = 0; i < sideCount; i++) {
		float x = origin->x() + (dist) * cos(i * alpha);
		float y = origin->y() + (dist) * sin(i * alpha);

		centerVertices->push_back(new QPointF(x, y));
	}
}

bool PoincareView::hasBeenDrawn(QPointF *aPoint) {
	int precision = pow(10,3);
	float x = round(precision * aPoint->x())/precision;
	float y = round(precision * aPoint->y())/precision;

	if(drawnTiles.count(x) == 1) {
		if(drawnTiles[x].count(y) == 1)
			return true;
	} else {
		drawnTiles[x] = std::unordered_set<float>();
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
	if(e){}
	this->diskDiameter = (int)std::min(size().width(), size().height()) - 10;
	this->painter = new QPainter(this);
	painter->setRenderHint(QPainter::HighQualityAntialiasing);
	this->diskPath = new QPainterPath();

	this->origin->setX(round(size().width()/2));
	this->origin->setY(round(size().height()/2));

	painter->setPen(QPen(QColor(122, 0, 127, 255), 2));
	this->diskRegion = new QRegion(QRect(origin->x() - diskDiameter/2, origin->y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion::Ellipse);
	diskPath->addRegion(*diskRegion);
	painter->setClipRegion(*diskRegion);

	genCenterVertices();
	drawTile(this->centerVertices, this->origin, this->renderLayers);

	painter->setClipping(false);

	int diskCenterX = -diskDiameter/2 + origin->x();
	int diskCenterY = -diskDiameter/2 + origin->y();
	painter->setPen(QPen(QColor(5, 0, 127, 255), 3));
	painter->drawEllipse(QRect(diskCenterX, diskCenterY, diskDiameter, diskDiameter));

	painter->end();
	std::cout << drawnCount << std::endl;

	delete this->diskPath;
	this->drawnCount = 0;
	this->drawnTiles.clear();
	this->centerVertices->clear();
}
