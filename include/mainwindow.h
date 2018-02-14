#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPainter>
#include <QRegion>
#include <QPainterPath>
#include <map>
#include <vector>

namespace Ui {
class MainWindow;
}
struct circle_t {
    QPointF *center;
    float radius;
};

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;


protected:
    int sideCount;
    int adjacentCount;
    int diskDiameter;
    QPointF *origin;
    QRegion *diskRegion;
    QPainter *painter;
    QVector<QPointF> getCenterVertices();
    QPointF *reflectPointAbout(QPointF *aPoint, circle_t aCircle);
    circle_t getCircleFromPoints(QPointF a, QPointF b);
    void paintEvent(QPaintEvent *e);
};

#endif // MAINWINDOW_H
