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

class PoincareView : public QOpenGLWidget {

public:
    explicit PoincareView(QWidget *parent);
    virtual ~PoincareView();

protected:
    u_int sideCount;
    u_int adjacentCount;
    u_int drawnCount;
    u_int renderLayers;
    int diskDiameter;
    std::map<float, std::unordered_set<float> > drawnTiles;

    QPainter *painter;
    QPointF *origin;
    QRegion *diskRegion;
    QPainterPath *diskPath;
    QVector<QPointF *> *centerVertices;

    void genCenterVertices();
    bool hasBeenDrawn(QPointF *aPoint);
    void drawTile(QVector<QPointF *> *vertices, QPointF *center, int layers);    
    void paintEvent(QPaintEvent *e);
};

#endif // POINCAREVIEW_H
