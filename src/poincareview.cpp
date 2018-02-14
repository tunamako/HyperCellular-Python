#include "poincareview.h"

#include <QWidget>
#include <QPainter>
#include <QPainterPath>
#include <QVector>
#include <QBrush>
#include <QRegion>

#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>

PoincareView::PoincareView(QWidget *parent) :
    QWidget(parent) {

    this->sideCount = 5;
    this->adjacentCount = 4;
}

PoincareView::~PoincareView(){}

float distance(QPointF a, QPointF b){
    return sqrt(pow((b.x() - a.x()), 2) + pow((b.y() - a.y()), 2));
}

double pointAngle(QPointF a, QPointF b) {
    return atan2(b.y() - a.y(), b.x() - a.x()) * 180/M_PI;
}

QPointF midpoint(QPointF a, QPointF b) {
    return QPointF((a.x() + b.x())/2, (a.y() + b.y())/2);
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

QPointF *PoincareView::reflectPointAbout(QPointF *aPoint, circle_t aCircle) {
    float x = aPoint->x();
    float y = aPoint->y();
    float x0 = aCircle.center->x();
    float y0 = aCircle.center->y();
    float invX = x0 + (pow(aCircle.radius, 2) * (x-x0)) / (pow(x-x0, 2) + pow(y-y0, 2));
    float invY = y0 + (pow(aCircle.radius, 2) * (y-y0)) / (pow(x-x0, 2) + pow(y-y0, 2));
    return new QPointF(invX, invY);
}

void PoincareView::drawTile(QVector<QPointF> vertices, int layers) {
    if(layers == 0)
        return;

    QVector<QPointF> reflectedVertices;
    circle_t invCircle;

    for(int i = 0; i < sideCount; i++) {
        if(i < sideCount - 1)
            invCircle = getCircleFromPoints(vertices[i], vertices[i+1]);
        else
            invCircle = getCircleFromPoints(vertices[i], vertices[0]);

        painter->drawEllipse(QRectF(invCircle.center->x() - invCircle.radius, invCircle.center->y() - invCircle.radius, invCircle.radius * 2, invCircle.radius * 2));
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
    painter->setPen(QPen(QColor(5, 0, 127, 255), 3));

    origin = new QPointF(size().width()/2, size().height()/2 );
    QRegion disk(QRect(origin->x() - diskDiameter/2, origin->y() - diskDiameter/2, diskDiameter, diskDiameter), QRegion::Ellipse);

    //Create Poincare Disk
    int diskCenterX = -diskDiameter/2 + origin->x();
    int diskCenterY = -diskDiameter/2 + origin->y();
    painter->drawEllipse(QRect(diskCenterX, diskCenterY, diskDiameter, diskDiameter));
    QVector<QPointF> centerVertices = getCenterVertices();
    painter->setPen(QPen(QColor(122, 0, 127, 255), 3));
    painter->setClipRegion(disk);

    drawTile(centerVertices, 4);
    painter->end();

}
