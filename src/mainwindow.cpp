#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QPainter>
#include <QPainterPath>
#include <QVector>
#include <QBrush>
#include <iostream>
#include <boost/math/constants/constants.hpp>
#include <math.h>
#include <vector>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {
    ui->setupUi(this);

    this->sideCount = 6;
    this->diskDiameter = 500;
}

MainWindow::~MainWindow() {
    delete ui;
}

float distance(QPoint a, QPoint b){
    return sqrt(pow((b.x() - a.x()), 2) + pow((b.y() - a.y()), 2));
}

double pointAngle(QPoint a, QPoint b) {
    return atan2(b.y() - a.y(), b.x() - a.x()) * 180/M_PI;
}

QPoint midpoint(QPoint a, QPoint b) {
    return QPoint((a.x() + b.x())/2, (a.y() + b.y())/2);
}

QVector<QPoint> MainWindow::getPolygonPoints() {
    QVector<QPoint> polygonPoints;
    float alpha = 2 * M_PI / sideCount;
    float padding = 2 * diskDiameter/(2 * sqrt(2)) - diskDiameter/2;
    int height = size().height();
    int width = size().width();

    for(int i = 0; i < sideCount; i++) {
        int x = width/2 + (diskDiameter/2 + padding) * cos(i * alpha);
        int y = height/2 + (diskDiameter/2 + padding) * sin(i * alpha);
        polygonPoints.push_back(QPoint(x, y));
    }
    return polygonPoints;
}

//Draw arcs with centers defined by centerPoints, and extra angle modifier specified by theta
QPainterPath *MainWindow::getArcsPath(QVector<QPoint> centerPoints, float radius, float theta) {
    QPainterPath *path = new QPainterPath();
    for(int i = 0; i < centerPoints.length(); i++) {
        QPoint A = centerPoints[i];
        QRectF rect = QRectF(A.x() - radius, A.y() - radius, 2 * radius, 2 * radius);
        float angleOffset = i * 360/sideCount;

        path->arcMoveTo(rect, -225 - angleOffset + 60 + theta);
        path->arcTo(rect, -225 - angleOffset + 60 + theta, -30);
    }
    path->closeSubpath();
    return path;
}

void MainWindow::paintEvent(QPaintEvent *e) {
    QPainterPath path;
    painter = new QPainter(this);
    painter->setRenderHint(QPainter::Antialiasing, true);

    QPoint origin = QPoint(size().width()/2, size().height()/2 );

    //Create Poincare Disk
    int diskCenterX = -diskDiameter/2 + origin.x();
    int diskCenterY = -diskDiameter/2 + origin.y();
    disk = QPainterPath();
    disk.addEllipse(QRect(diskCenterX, diskCenterY, diskDiameter, diskDiameter));
    path.closeSubpath();

    //Create main outer polygon
    QVector<QPoint> polygonPoints = getPolygonPoints();
    path = QPainterPath();
    path.addPolygon(QPolygonF(polygonPoints));
    path.closeSubpath();
    painter->setPen(QPen(QColor(5, 0, 127, 255), 2));
    painter->drawPath(path);

    //Create arcs centered around midpoints of polygon edges
    QVector<QPoint> polygonMidpoints;
    for(int i = 0; i < polygonPoints.length(); i++) {
        QPoint mid = (i == sideCount - 1)
                ? midpoint(polygonPoints[i], polygonPoints[0])
                : midpoint(polygonPoints[i], polygonPoints[i+1]);
        polygonMidpoints.push_back(QPoint(mid));
    }


    QPainterPath *arcs = getArcsPath(polygonMidpoints,
                                     distance(polygonPoints[0], polygonPoints[1])/2,
                                     asin(cos(2 * M_PI/(2 * (float)sideCount))) * 180/M_PI);
    painter->setPen(QPen(QColor(255, 0, 127, 255), 2));
    //painter->drawPath(*arcs);

    //Create mother arcs
    arcs = getArcsPath(polygonPoints, diskDiameter/2, 0);
    arcs->moveTo(QPoint(500, 500));
    painter->drawPath(*arcs);

    painter->fillPath(*arcs, QBrush(QColor(0, 255, 255, 255)));
    painter->setPen(QPen(QColor(0, 0, 0, 255), 2));
    painter->drawPath(disk);
}
