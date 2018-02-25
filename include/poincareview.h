#ifndef POINCAREVIEW_H
#define POINCAREVIEW_H

#include <QWidget>
#include <QPainter>
#include <QOpenGLWidget>
#include <QPainterPath>


#include <string>
#include <map>
#include <unordered_set>

namespace Ui {
class PoincareView;
}

struct circle_t {
    QPointF *center;
    double radius;
};

struct line_t {
	double y_intercept;
	double slope;
};

class PoincareView : public QOpenGLWidget {

public:
    explicit PoincareView(QWidget *parent);
    virtual ~PoincareView();

protected:
    int sideCount;
    int adjacentCount;
    int diskDiameter;
    int drawnCount;
    int renderLayers;
    std::map<double, std::unordered_set<double> > drawnTiles;

    QPainter *painter;
    QPointF *origin;
    QRegion *diskRegion;
    QPainterPath *diskPath;

    QVector<QPointF *> *getCenterVertices();
    QPointF *reflectAboutArc(QPointF *aPoint, circle_t aCircle);
    QPointF *reflectAboutLine(QPointF *aPoint, line_t aLine);
    bool hasBeenDrawn(QPointF *aPoint);
    void drawArc(QPointF A, QPointF B, circle_t circle);
    void drawTile(QVector<QPointF *> *vertices, QPointF *center, int layers);    
    void paintEvent(QPaintEvent *e);
};

#endif // POINCAREVIEW_H
