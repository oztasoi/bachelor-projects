#ifndef INITIALSCREEN_H
#define INITIALSCREEN_H

#include <QDialog>
#include <mainwindow.h>
#include <QSound>

namespace Ui {
class InitialScreen;
}

class InitialScreen : public QDialog
{
    Q_OBJECT

public:
    explicit InitialScreen(QWidget *parent = nullptr);
    ~InitialScreen();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::InitialScreen *ui;
    MainWindow *mwindow;
};

#endif // INITIALSCREEN_H
