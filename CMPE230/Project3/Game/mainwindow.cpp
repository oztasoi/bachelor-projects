#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QList<QAbstractButton*> bts = ui->buttonGroup->buttons();

    this->pairs = 0;
    this->tries = 0;
    this->remaniningcards = 24; // remaining number of cards;
    randomize();
    for(int i=0;i<24;i++){
        QObject::connect(bts[i], SIGNAL(clicked()), this, SLOT(buttonClicked())); //each button is constructed via signal/slot pair;
    }
    QObject::connect(ui->Reset, SIGNAL(clicked()), this, SLOT(on_Reset_clicked())); //reset button is constructed;
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::buttonClicked(){
    if(this->buttoncount == 0){ //checks how many button is clicked;
        this->prebutton = (QPushButton *)sender(); //finds which button is pressed;
        QString buttonName = this->prebutton->objectName();
        QString buttonNumber = buttonName.split("_")[1]; //finds the current number of first button;
        this->prestring = this->letters[buttonNumber.toInt()-1]; //turns it to index number of array;
        this->prebutton->setText(this->prestring); //changes the text on button;
        this->prebutton->setDisabled(true); //disables the button to prevent consecutive clicks on same button;
        this->buttoncount = 1; //increases button count;
    }
    else {
        this->curbutton = (QPushButton *)sender();
        QString buttonName = this->curbutton->objectName(); //same;
        QString buttonNumber = buttonName.split("_")[1]; //finds the current number of second button;
        this->curstring = this->letters[buttonNumber.toInt()-1]; //finds the second index;
        this->curbutton->setText(this->curstring); //changes the text on button;
        this->curbutton->setDisabled(true); //same logic above;
        this->buttoncount = 0; //resets the counter;
        ui->trieslcd->display(QString::number(++tries));//increases tries by 1;
        ui->centralWidget->setDisabled(true); //disables all clickable components to prevent malicious usage;
        QTest::qWait(1000); //waits to show the current state to end user;
        ui->centralWidget->setEnabled(true); //enables all clickable components to be used;
        if(prestring == curstring){ //checks if the two characters are same;
            ui->pairslcd->display(QString::number(++pairs)); //by correct pair, increases the pairs by 1;
            this->prebutton->setText(""); //changes text in button 1;
            this->curbutton->setText(""); //changes text in button 2;
            this->prebutton->setDisabled(true); //disables the button 1;
            this->curbutton->setDisabled(true); //disables the button 2;
            this->remaniningcards = this->remaniningcards - 2; //decreases the remaining card by 2;
            if(this->remaniningcards == 0){ // checks if the game ends;
                afterscr = new AfterScreen(this);
                afterscr->show();
                this->hide();
            }
        } else {
            this->prebutton->setText("X"); //set "X" for button;
            this->curbutton->setText("X"); //same as above;
            this->prebutton->setEnabled(true); //enables the button to be pressed again;
            this->curbutton->setEnabled(true); //same as above;
        }
    }
}

// randomly shuffles the array to be used again;
void MainWindow::randomize(){
    this->letters = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"};
    qsrand(time(NULL));
    std::random_shuffle(letters.begin(),letters.end());
}

void MainWindow::on_Reset_clicked()
{
        QList<QAbstractButton*> refreshedbuttonslist = ui->buttonGroup->buttons(); //gets the refreshed buttons list;
        randomize(); //randomly shuffles all cards;
        for(int i=0;i<24;i++){
            refreshedbuttonslist[i]->setEnabled(true); //set enable to all buttons;
            refreshedbuttonslist[i]->setText("X"); //set buttons to show "X";
        }
        this->remaniningcards = 24;
        this->pairs = 0; //sets the pairs lcd;
        this->tries = 0; //same as above;
        ui->pairslcd->display(QString::number(pairs)); //shows the current state for pairs;
        ui->trieslcd->display(QString::number(tries)); //same as above for tries;
}
