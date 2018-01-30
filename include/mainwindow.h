#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPainter>

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
    QPainter *painter;
    QPoint* getPolygonPoints(int padding);
    void paintEvent(QPaintEvent *e);
};

#endif // MAINWINDOW_H
