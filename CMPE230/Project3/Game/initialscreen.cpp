#include "initialscreen.h"
#include "ui_initialscreen.h"

InitialScreen::InitialScreen(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::InitialScreen)
{
    ui->setupUi(this);
}

InitialScreen::~InitialScreen()
{
    delete ui;
}

void InitialScreen::on_pushButton_clicked()
{
    this->hide();
    mwindow = new MainWindow(this);
    mwindow->show();
}

void InitialScreen::on_pushButton_2_clicked()
{
    this->close();
}
