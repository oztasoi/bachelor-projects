#include "LinkedList.h"

LinkedList::LinkedList() {
    length = 0;
    head = tail = nullptr;
}

LinkedList::LinkedList(const LinkedList& list){


    this->head = new Node(*(list.head));
    Node* tailTracer = this->head;
    while(tailTracer->next){
        tailTracer = tailTracer->next;
    }
    this->tail = tailTracer;
    this->length = list.length;
}

LinkedList::LinkedList(LinkedList &&list) {

    this->head = move(list.head);
    Node* tailTracer = this->head;
    while(tailTracer->next){
        tailTracer = tailTracer->next;
    }
    this->tail = tailTracer;
    this->length = list.length;

    list.head = nullptr;
    list.tail = nullptr;
    list.length = 0;

}

LinkedList& LinkedList::operator=(LinkedList &&list) {

    this->head = move(list.head);
    Node* tailTracer = this->head;
    while(tailTracer->next){
        tailTracer = tailTracer->next;
    }
    this->tail = tailTracer;
    this->length = move(list.length);
    list.head = nullptr;
    list.tail = nullptr;
    list.length = 0;
    return *this;
}

LinkedList& LinkedList::operator=(const LinkedList &list) {

    this->head->~Node();
    this->head = new Node(*list.head);
    Node* tailTracer = this->head;
    while(tailTracer->next){
        tailTracer = tailTracer->next;
    }
    this->tail = tailTracer;
    this->length = list.length;
    return *this;

}

void LinkedList::pushTail(string _name, float _amount) {
    if(!this->head){
        this->head = new Node(_name,_amount);
        this->tail = this->head;
    } else {
        tail->next = new Node(_name, _amount);
        tail = tail->next;
        this->length++;
    }
}

void LinkedList::updateNode(string _name, float _amount) {
    Node* tracer = this->head;
    while(tracer){
        if(tracer->name == _name){
            tracer->amount = _amount;
            return;
        }
        tracer = tracer->next;
    }
    pushTail(_name,_amount);
}

LinkedList::~LinkedList() {

    delete this->head;
    this->tail = nullptr;
    this->length = 0;
}
