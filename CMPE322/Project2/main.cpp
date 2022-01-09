#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <time.h>
#include <map>
#include <queue>

#define BIAS 1000000 // bias value to prepare the nanosleep() 

using namespace std;

map<string, pthread_mutex_t> isBillTypeUsed; // mutex for type.
pthread_mutex_t isPenBusy = PTHREAD_MUTEX_INITIALIZER; // mutex for writing the file..
pthread_mutex_t isAtmUsed[10]; // mutex for atm usage.
pthread_cond_t wakey[10]; // condition variable to wake related atm.
pthread_cond_t jobDone[300]; // condition variable to wake related customer.
pthread_mutex_t cihat = PTHREAD_MUTEX_INITIALIZER;

int b_thread_id[300]; // holds the thread number for each thread to print.
int b_price[300]; // holds the bill price of each bill.
string b_type[300]; // holds the bill type of each bill.

int processed_threads = 0; // value of processed threads, used in check conditions.

map<string, int> totalBillAmount; // data structure that holds total for each bill type.

string destination; // output file destination.

struct atm_data{
    int atm_id;
    int total;
};

struct customer_data{
    int customer_id;
    string* customer_info;
};

void initBillTypeLocks(); // initializer of type mutex locks.

void initAtmLocks(); // initializer of atm mutex locks.

void initBillAmounts(); // initializer of type amounts.

void initJobDone(); // initializer of job state.

string tokenizer(); // converts string 

void *pay(void *payment_info); // atm thread function

void *define(void *customer_info); // customer thread function

int customer_count(char* source);

string* readInput(string* list, char* source);

int main(int argc, char* argv[]){

    int queue_length;
    string* customers;

    initBillTypeLocks();
    initBillAmounts();
    initAtmLocks();

    string dest = argv[1];
    destination = dest.substr(0, dest.length() - 4) + "_log.txt";

    ofstream os(destination);
    os << "";
    os.close();

    queue_length = customer_count(argv[1]);
    customers = readInput(customers, argv[1]);

    pthread_t customer_threads[queue_length];
    pthread_t atm_threads[10];
    struct customer_data cd[queue_length];
    struct atm_data ad[10];

    int err;

    for(int i=0; i<10; i++){
        ad[i].atm_id = i;
        ad[i].total = queue_length;

        err = pthread_create(&atm_threads[i], NULL, pay, (void*)&ad[i]);
        if(err){
            exit(-1);
        }
    }

    for(int i=0; i<queue_length; i++){
        cd[i].customer_id = i;
        cd[i].customer_info = &customers[i];

        err = pthread_create(&customer_threads[i], NULL, define, (void*)&cd[i]);
        if(err){
            exit(-1);
        }
    }

    for(int i=0; i<queue_length; i++){
        err = pthread_join(customer_threads[i], NULL);
    }

    while(processed_threads != queue_length);
    for(int i=0; i<10; i++){
        err = pthread_cancel(atm_threads[i]);
        if(err){
            exit(-1);
        }
    }

    ofstream ofs(destination, ofstream::app);

    ofs << "All payments are completed." << endl;
    ofs << "CableTV: " << totalBillAmount["cableTV"] << "TL" << endl;
    ofs << "Electricity: " << totalBillAmount["electricity"] << "TL" << endl;
    ofs << "Gas: " << totalBillAmount["gas"] << "TL" << endl;
    ofs << "Telecommunication: " << totalBillAmount["telecommunication"] << "TL" << endl;
    ofs << "Water: " << totalBillAmount["water"] << "TL" << endl;

    ofs.close();
    
    return 0;
}

void initBillTypeLocks(){
    isBillTypeUsed["cableTV"] = PTHREAD_MUTEX_INITIALIZER;
    isBillTypeUsed["electricity"] = PTHREAD_MUTEX_INITIALIZER;
    isBillTypeUsed["gas"] = PTHREAD_MUTEX_INITIALIZER;
    isBillTypeUsed["telecommunication"] = PTHREAD_MUTEX_INITIALIZER;
    isBillTypeUsed["water"] = PTHREAD_MUTEX_INITIALIZER;
}

void initAtmLocks(){
    for(int i=0; i<10; i++){
        isAtmUsed[i] = PTHREAD_MUTEX_INITIALIZER;
        wakey[i] = PTHREAD_COND_INITIALIZER;
    }
}

void initJobDone(){
    for(int i=0; i<300; i++){
        jobDone[i] = PTHREAD_COND_INITIALIZER;
    }
}

void initBillAmounts(){
    totalBillAmount["cableTV"] = 0;
    totalBillAmount["electricity"] = 0;
    totalBillAmount["gas"] = 0;
    totalBillAmount["telecommunication"] = 0;
    totalBillAmount["water"] = 0;
}

string tokenizer(string s){
    int index = s.find(",");
    return s.substr(0, index);
}

void *pay(void *payment_info){
    struct atm_data *current;
    current = (struct atm_data *)payment_info;
    
    while(processed_threads < current->total){
      
        pthread_cond_wait(&wakey[current->atm_id], &isAtmUsed[current->atm_id]);

        int thread_id = b_thread_id[current->atm_id];
        int price = b_price[current->atm_id];
        string type = b_type[current->atm_id];

        pthread_mutex_lock(&isBillTypeUsed[type]);
        totalBillAmount[type] += price;

        pthread_mutex_lock(&isPenBusy);

        ofstream ofs(destination, ofstream::app);
        ofs << "Customer" << (thread_id+1) << "," << price << "TL," << type << endl;
        ofs.close();

        pthread_mutex_unlock(&isPenBusy);
        pthread_mutex_unlock(&isBillTypeUsed[type]);
        
        pthread_cond_signal(&jobDone[processed_threads]);
    }
    pthread_exit(0);
}

void *define(void *customer_info){
    struct customer_data *current;
    current = (struct customer_data *)customer_info;

    string input = *(current->customer_info);
    string sliced_input[4];
    
    for(int i=0; i<3; i++){
        sliced_input[i] = tokenizer(input);
        input = input.substr(sliced_input[i].length()+1, input.length());
    }
    sliced_input[3] = input;

    int wait_time = stoi(sliced_input[0]);
    int atm_index = stoi(sliced_input[1]) - 1;
    string type = sliced_input[2];
    int bill_amount = stoi(sliced_input[3]);

    struct timespec ts;
    ts.tv_sec = 0;
    ts.tv_nsec = (BIAS * wait_time);

    nanosleep(&ts, NULL);
    pthread_mutex_lock(&isAtmUsed[atm_index]);
    
    b_thread_id[atm_index] = current->customer_id;
    b_price[atm_index] = bill_amount;
    b_type[atm_index] = type;

    pthread_mutex_lock(&cihat);
    processed_threads += 1;
    pthread_mutex_unlock(&cihat);
    pthread_mutex_unlock(&isAtmUsed[atm_index]);
    pthread_cond_signal(&wakey[atm_index]);
    pthread_exit(0);
}

int customer_count(char* source){
    
    ifstream ifs(source);
    string c_count;
    ifs >> c_count;
    ifs.close();
    return stoi(c_count);
}

string* readInput(string* list, char* source){
    
    ifstream ifs(source);
    string customer_count;
    ifs >> customer_count; // get the customer count from the input.
    int cc = stoi(customer_count);
    
    list = new string[cc]; // define the pointer as the start point of string array.
    string current_customer;
    for(int i=0; i<cc; i++){
        ifs >> list[i]; // fill the array with the input.
    }
    ifs.close();
    return list; // return the pointer of string array.
}
