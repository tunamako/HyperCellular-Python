#include "mainwindow.h"
#include "forms/ui_mainwindow.h"

#include <QPainter>
#include <QPainterPath>
#include <QVector>
#include <QBrush>
#include <QRegion>

#include <iostream>
#include <math.h>
#include <vector>


MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
	delete ui;
}