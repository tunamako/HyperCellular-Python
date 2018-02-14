#ifndef POINCAREVIEW_H
#define POINCAREVIEW_H
#include <QWidget>
#include <QPainter>

namespace Ui {
class PoincareView;
}
struct circle_t {
    QPointF *center;
    float radius;
};

class PoincareView : public QWidget {

public:
    explicit PoincareView(QWidget *parent);
    virtual ~PoincareView();

protected:
    int sideCount;
    int adjacentCount;
    int diskDiameter;
    QPainter *painter;
    QPointF *origin;

    QVector<QPointF> getCenterVertices();
    QPointF *reflectPointAbout(QPointF *aPoint, circle_t aCircle);
    circle_t getCircleFromPoints(QPointF a, QPointF b);
    void drawTile(QVector<QPointF> vertices, int layers);    void paintEvent(QPaintEvent *e);
};

#endif // POINCAREVIEW_H
