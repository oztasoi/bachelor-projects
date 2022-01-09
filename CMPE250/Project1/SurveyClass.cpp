#include "SurveyClass.h"


SurveyClass::SurveyClass() {
    this->members = new LinkedList();
}

SurveyClass::SurveyClass(const SurveyClass &other) {
    this->members = new LinkedList(*other.members);
    this->members->length = other.members->length;
}

SurveyClass::SurveyClass(SurveyClass &&other) {
    this->members = move(other.members);
    this->members->length = move(other.members->length);
    other.members = nullptr;
    other.members->length = 0;

}

SurveyClass& SurveyClass::operator=(const SurveyClass &list) {
    this->members->~LinkedList();
    this->members = new LinkedList(*list.members);
    this->members->length = list.members->length;
    return *this;
}

SurveyClass& SurveyClass::operator=(SurveyClass &&list) {
    this->members = std::move(list.members);
    this->members->length = list.members->length;
    list.members->length = 0;
    list.members = nullptr;
    return *this;
}

SurveyClass::~SurveyClass() {
    this->members->~LinkedList();
}

float SurveyClass::calculateMinimumExpense() {

    Node* tracer = this->members->head;
    float min = tracer->amount;
    while(tracer){
        if(tracer->amount < min){
            min = tracer->amount;
        }
        tracer = tracer->next;
    }

    return (int)((min*100))/100.0;
}

float SurveyClass::calculateMaximumExpense() {
    float max = 0;
    Node* tracer = members->head;
    while(tracer){
        if(tracer->amount > max){
            max = tracer->amount;
        }
        tracer = tracer->next;
    }

    return (int)((max*100))/100.0;
}

float SurveyClass::calculateAverageExpense() {
    Node* tracer = this->members->head;
    float sum = 0;
    int count = 0;
    while(tracer){
        sum += tracer->amount;
        tracer = tracer->next;
        count++;
    }
    cout << sum << endl;
    cout << count << endl;
    return (int)((sum/count)*100)/100.0;

}

void SurveyClass::handleNewRecord(string _name, float _amount) {
    if(!members->head){
        members->head = new Node(_name,_amount);
        members->tail = members->head;
    } else {
        this->members->updateNode(_name,_amount);
    }
}
