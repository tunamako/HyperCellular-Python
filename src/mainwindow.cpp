#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QPainter>
#include <iostream>
#include <boost/math/constants/constants.hpp>
#include <math.h>

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

QPoint* MainWindow::getPolygonPoints(int padding) {
    QPoint *polygonPoints = new QPoint[sideCount];
    float alpha = 2 * M_PI / sideCount;
    int height = size().height();
    int width = size().width();

    for(int i = 0; i < sideCount; i++) {
        int x = width/2 + (diskDiameter/2 + padding) * cos(i * alpha);
        int y = height/2 + (diskDiameter/2 + padding) * sin(i * alpha);
        polygonPoints[i] = QPoint(x, y);
    }
    return polygonPoints;
}

void MainWindow::paintEvent(QPaintEvent *e) {
    this->painter = new QPainter(this);
    painter->setPen(QPen(QColor(5, 0, 127, 255), 2));
    painter->setRenderHint(QPainter::Antialiasing, true);
    QPoint origin = QPoint(size().width()/2, size().height()/2 );
    int circleX = -diskDiameter/2 + origin.x();
    int circleY = -diskDiameter/2 + origin.y();

    painter->drawEllipse(QRect(circleX, circleY, diskDiameter, diskDiameter));

    QPoint *polygonPoints = getPolygonPoints(150);
    painter->drawPolygon(polygonPoints, sideCount);


    for(int i = 0; i < sideCount; i++) {
        QPoint A, B;
        if(i == sideCount - 1) {
            A = polygonPoints[i];
            B = polygonPoints[0];
        } else {
            A = polygonPoints[i];
            B = polygonPoints[i + 1];
        }
        QPoint mid = midpoint(A, B);
        float arcDiameter = distance(A, B);
        painter->translate(mid.x(), mid.y());
        painter->rotate(pointAngle(A, B));

        painter->drawArc(QRectF(-arcDiameter/2, -arcDiameter/2, arcDiameter, arcDiameter), 0, -16 * 180);
        painter->resetTransform();

    }
}
