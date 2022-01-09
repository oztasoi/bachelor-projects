#include "afterscreen.h"
#include "ui_afterscreen.h"

AfterScreen::AfterScreen(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AfterScreen)
{
    ui->setupUi(this);
}

AfterScreen::~AfterScreen()
{
    delete ui;
}

void AfterScreen::on_pushButton_clicked()
{
    this->close(); // ends the game;
}
