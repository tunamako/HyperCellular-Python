#include "poincareview.h"

#include <QWidget>
#include <QPainter>
#include <QPainterPath>
#include <QVector>
#include <QBrush>
#include <QRegion>

#include <QOpenGLFunctions>

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>
#include <set>
#include <tuple>

PoincareView::PoincareView(QWidget *parent) :
	QOpenGLWidget(parent) {

	drawnTiles = std::set<two_tuple>();
	this->sideCount = 7;
	this->adjacentCount = 3;
}
PoincareView::~PoincareView(){}

float distance(QPointF a, QPointF b){
	return sqrt(pow((b.x() - a.x()), 2) + pow((b.y() - a.y()), 2));
}

QPointF midpoint(QPointF a, QPointF b) {
	return QPointF((a.x() + b.x())/2, (a.y() + b.y())/2);
}

bool areCollinear(QPointF a, QPointF b, QPointF c) {
	QLineF AB(a, b);
	QLineF BC(b, c);
	QLineF AC(a, c);
	return ceil(AB.angleTo(BC)) == ceil(AB.angleTo(AC));
}

circle_t PoincareView::getCircleFromPoints(QPointF a, QPointF b) {
	circle_t disk;
	disk.center = origin;
	disk.radius = diskDiameter/2;
	QPointF c = *reflectPointAbout(&a, disk);

	a.setX(a.x()-c.x());
	a.setY(a.y()-c.y());
	b.setX(b.x()-c.x());
	b.setY(b.y()-c.y());

	float Z1 = a.x() * a.x() + a.y() * a.y();
	float Z2 = b.x() * b.x() + b.y() * b.y();
	float D = 2 * (a.x() * b.y() - b.x() * a.y());

	float centerX = (Z1 * b.y() - Z2 * a.y()) / D + c.x();
	float centerY = (a.x() * Z2 - b.x() * Z1) / D + c.y();


	circle_t circ;
	circ.center = new QPointF(centerX, centerY);
	circ.radius = distance(*circ.center, c);

	return circ;
}

QVector<QPointF> PoincareView::getCenterVertices() {
	QVector<QPointF> vertices;
	int p = sideCount;
	int q = adjacentCount;
	float dist = (diskDiameter/2) * sqrt(cos(M_PI/p + M_PI/q)*cos(M_PI/q) / (sin(2*M_PI/q) * sin(M_PI/p) + cos(M_PI/p + M_PI/q)* cos(M_PI/q)));
	float alpha = 2 * M_PI / sideCount;

	for(int i = 0; i < sideCount; i++) {
		float x = origin->x() + (dist) * cos(i * alpha);
		float y = origin->y() + (dist) * sin(i * alpha);
		vertices.push_back(QPointF(x, y));
	}
	return vertices;
}

QPointF *PoincareView::reflectPointAbout(QPointF *A, circle_t aCircle) {
	float x = A->x();
	float y = A->y();
	float x0 = aCircle.center->x();
	float y0 = aCircle.center->y();
	float invX = x0 + (pow(aCircle.radius, 2) * (x-x0)) / (pow(x-x0, 2) + pow(y-y0, 2));
	float invY = y0 + (pow(aCircle.radius, 2) * (y-y0)) / (pow(x-x0, 2) + pow(y-y0, 2));
	return new QPointF(invX, invY);
}

void PoincareView::drawArc(QPointF A, QPointF B, circle_t aCircle) {
	//rectangle inscribed by aCircle
	QRectF rect(aCircle.center->x() - aCircle.radius, aCircle.center->y() - aCircle.radius, aCircle.radius * 2, aCircle.radius * 2);
	QLineF lineA(*aCircle.center, A);
	QLineF lineB(*aCircle.center, B);

	float sweepAngle = lineA.angleTo(lineB);
	if(sweepAngle > 180)
		sweepAngle -= 360;

	painter->drawArc(rect, 16 * lineA.angle(), 16 * sweepAngle);
	painter->drawPoint(A);
	painter->drawPoint(B);
}

void PoincareView::drawTile(QVector<QPointF> vertices, int layers) {
	if(layers == 0)
		return;

	QVector<QPointF> reflectedVertices;
	float centroidX = 0;
	float centroidY = 0;

	//First verify if this tile has been drawn before: this is very sloppy and inaccurate at deeper levels
	/*
	for(int i = 0; i < sideCount; i++) {
		centroidX += vertices[i].x();
		centroidY += vertices[i].y();
	}
	two_tuple centroid = two_tuple(centroidX/sideCount, centroidY/sideCount);
	auto search = drawnTiles.find(centroid);
	if(search != drawnTiles.end())
		return;
	else
		drawnTiles.insert(centroid);
	*/

	//Circle which contains the arc/axis of reflection, used to invert points
	circle_t invCircle;
	//Draw and reflect across each side of this tile
	for(int i = 0; i < sideCount; i++) {
		QPointF A = vertices[i];
		QPointF B = (i < sideCount - 1)
			? vertices[i+1]
			: vertices[0];

		if(areCollinear(A, B, *origin)) {
			painter->drawLine(A, B);
		} else {
			invCircle = getCircleFromPoints(A, B);
			drawArc(A, B, invCircle);
		}

		reflectedVertices = QVector<QPointF>();
		for(int j = 0; j < sideCount; j++) {
			reflectedVertices.push_back(*reflectPointAbout(&vertices[j], invCircle));
		}
		drawTile(reflectedVertices, layers-1);
	}

}

void PoincareView::paintEvent(QPaintEvent *e) {
	this->diskDiameter = std::min(size().width(), size().height()) - 10;
	painter = new QPainter(this);
	painter->setRenderHint(QPainter::HighQualityAntialiasing);
	origin = new QPointF(size().width()/2, size().height()/2 );

	QVector<QPointF> centerVertices = getCenterVertices();
	painter->setPen(QPen(QColor(122, 0, 127, 255), 2));
	QRegion disk(QRect(origin->x() - diskDiameter/2, origin->y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion::Ellipse);
	painter->setClipRegion(disk);
	
	drawTile(centerVertices, 5);

	painter->setClipping(false);
	int diskCenterX = -diskDiameter/2 + origin->x();
	int diskCenterY = -diskDiameter/2 + origin->y();
	painter->setPen(QPen(QColor(5, 0, 127, 255), 3));
	painter->drawEllipse(QRect(diskCenterX, diskCenterY, diskDiameter, diskDiameter));

	painter->end();
	std::cout << drawnTiles.size() << std::endl;
	drawnTiles.clear();
}
