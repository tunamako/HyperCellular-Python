#ifndef POINCAREVIEW_H
#define POINCAREVIEW_H
#include <QWidget>
#include <QPainter>
#include <QOpenGLWidget>

#include <tuple>
#include <set>

namespace Ui {
class PoincareView;
}

struct circle_t {
    QPointF *center;
    float radius;
};

typedef std::tuple<float, float> two_tuple;

class PoincareView : public QOpenGLWidget {

public:
    explicit PoincareView(QWidget *parent);
    virtual ~PoincareView();

protected:
    int sideCount;
    int adjacentCount;
    int diskDiameter;
    std::set<two_tuple> drawnTiles;

    QPainter *painter;
    QPointF *origin;

    QVector<QPointF> getCenterVertices();
    QPointF *reflectPointAbout(QPointF *aPoint, circle_t aCircle);
    circle_t getCircleFromPoints(QPointF a, QPointF b);
    void drawArc(QPointF A, QPointF B, circle_t circle);
    void drawTile(QVector<QPointF> vertices, int layers);    
    void paintEvent(QPaintEvent *e);
};

#endif // POINCAREVIEW_H
