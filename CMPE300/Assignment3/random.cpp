#include <stdlib.h>
#include <stdio.h>
#include <time.h>

bool isIn(double x, double y){
    return (x*x + y*y < 1) and ((x-1)*(x-1) + y*y < 1) and (x*x + (y-1)*(y-1) < 1) and ((x-1)*(x-1) + (y-1)*(y-1) < 1);
}

int main(){
    srand(time(NULL));

    double x[20];
    double y[20];
    int hit = 0;

    for(int i=0; i< 20; i++){
        x[i] = (double)rand()/RAND_MAX;
        y[i] = (double)rand()/RAND_MAX;
    }

    for(int i=0; i<20; i++){
        if(isIn(x[i], y[i])){
            hit = hit + 1;
            printf("%f %f Inside.\n", x[i], y[i]);
        }
        else{
            printf("%f %f\n", x[i], y[i]);
        }
    }
    
    printf("%f\n", hit/(double)20);
    return 0;
}