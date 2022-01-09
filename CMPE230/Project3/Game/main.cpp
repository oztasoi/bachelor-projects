#include "initialscreen.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    InitialScreen inscreen;
    inscreen.show();

    return a.exec();
}
