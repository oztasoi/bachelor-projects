#ifndef AFTERSCREEN_H
#define AFTERSCREEN_H

#include <QDialog>
#include <QWidget>


namespace Ui {
class AfterScreen;
}

class AfterScreen : public QDialog
{
    Q_OBJECT

public:
    explicit AfterScreen(QWidget *parent = nullptr);
    ~AfterScreen();

private slots:
    void on_pushButton_clicked();

private:
    Ui::AfterScreen *ui;
};

#endif // AFTERSCREEN_H
