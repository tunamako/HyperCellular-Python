#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPainter>
#include <QPainterPath>
#include <map>
#include <vector>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;


protected:
    int sideCount;
    int diskDiameter;
    QPainterPath disk;
    QPainter *painter;
    QVector<QPoint> getPolygonPoints();
    QPainterPath *getArcsPath(QVector<QPoint> centerPoints, float radius, float theta);
    void paintEvent(QPaintEvent *e);
};

#endif // MAINWINDOW_H
