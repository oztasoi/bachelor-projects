#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QAbstractButton>
#include <QTest>
#include "afterscreen.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui; //current ui;
    QPushButton *prebutton; //previously clicked button;
    QPushButton *curbutton; //currently clicked button;
    int buttoncount = 0; //shows how many buttons are clicked in current state;
    QList<QString> letters; //cards;
    QString prestring; // card of previously clicked button;
    QString curstring; // card of currently clicked button;
    int pairs; // number of pairs found;
    int tries; // number of tries attempted;
    int remaniningcards; // number of remaining cards;
    AfterScreen *afterscr; // afterscreen of the end of the game;
    void randomize(); // card shuffling function;

private slots:
    void buttonClicked(); // slot for cards;
    void on_Reset_clicked(); // slot for reset button;
};

#endif // MAINWINDOW_H
