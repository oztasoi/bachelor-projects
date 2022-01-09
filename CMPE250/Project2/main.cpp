#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int TIME = 1;

class Passenger{
public:
    int arrival_time;
    int departure_time;
    int luggage_desk_time;
    int security_desk_time;
    char is_vip;
    char is_ocu;

    Passenger(){
        this->arrival_time = 0;
        this->departure_time = 0;
        this->luggage_desk_time = 0;
        this->security_desk_time = 0;
        this->is_vip = 0;
        this->is_ocu = 0;
    }

    Passenger(int _arrival_time, int _desired_departure_time, int _luggage_desk_time, int _security_desk_time, char _is_vip, char _is_ocu){
        this->arrival_time = _arrival_time;
        this->departure_time = _desired_departure_time;
        this->luggage_desk_time = _luggage_desk_time;
        this->security_desk_time = _security_desk_time;
        this->is_vip = _is_vip;
        this->is_ocu = _is_ocu;

    }

    ~Passenger(){
    }
};

class Event{
public:
    enum EVENT_TYPE{
        ARRIVAL = 1,
        LUGGAGE_EXIT = 2,
        SECURITY_EXIT = 3,
    };

    int time;
    Passenger current_passenger ;
    EVENT_TYPE current_type ;

    Event(int _time, Passenger _current_passenger, EVENT_TYPE _current_type){
        this->time = _time;
        this->current_passenger = _current_passenger;
        this->current_type = _current_type;

    }
    ~Event(){
    }
};

struct Compare_Departure{
    bool operator()(const Passenger &_p1, const Passenger &_p2){
        if(_p1.departure_time != _p2.departure_time){
            return _p1.departure_time > _p2.departure_time;
        } else {
            return _p1.arrival_time > _p2.arrival_time;
        }
    }
};

struct Compare_Event{
public:
    bool operator()(const Event &_e1, const Event &_e2){
        if(_e1.time != _e2.time){
            return _e1.time > _e2.time;
        }
        else if(_e1.current_type != _e2.current_type){
            return _e1.current_type < _e2.current_type;
        }
        else {
            return _e1.current_passenger.arrival_time > _e2.current_passenger.arrival_time;
        }
    }
};

int main(int argc, char* argv[]) {

    freopen(argv[1],"r",stdin);
    freopen(argv[2],"w+",stdout);

    long long int number_of_passengers;
    int number_of_luggage_counters;
    int number_of_security_counters;

    long long int total_minute_passed = 0;
    long long int missed_flights = 0;

    queue<Passenger> luggage_queue;
    queue<Passenger> security_queue;
    priority_queue<Passenger,vector<Passenger>,Compare_Departure> luggage_queue_;
    priority_queue<Passenger,vector<Passenger>,Compare_Departure> security_queue_;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_1;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_2;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_3;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_4;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_5;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_6;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_7;
    priority_queue<Event,vector<Event>,Compare_Event> event_queue_case_8;

    cin >> number_of_passengers >> number_of_luggage_counters >> number_of_security_counters;
    for(int i=0;i<number_of_passengers;i++){
        int arrival_time,desired_departure_time,luggage_desk_time,security_desk_time;
        char is_vip,is_ocu;
        scanf("%d %d %d %d %c %c",&arrival_time,&desired_departure_time,&luggage_desk_time,&security_desk_time,&is_vip,&is_ocu);
        Event* outgoing_event = new Event(arrival_time,*new Passenger(arrival_time,desired_departure_time,luggage_desk_time,security_desk_time,is_vip,is_ocu),Event::ARRIVAL);
        event_queue_case_1.push(*outgoing_event);
        event_queue_case_2.push(*outgoing_event);
        event_queue_case_3.push(*outgoing_event);
        event_queue_case_4.push(*outgoing_event);
        event_queue_case_5.push(*outgoing_event);
        event_queue_case_6.push(*outgoing_event);
        event_queue_case_7.push(*outgoing_event);
        event_queue_case_8.push(*outgoing_event);
    }


    //case 1:
    while(event_queue_case_1.size()){
        Event current_event = event_queue_case_1.top();
        event_queue_case_1.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            luggage_queue.push(current_event.current_passenger);
                if(number_of_luggage_counters > 0) {
                    Passenger a = luggage_queue.front();
                    luggage_queue.pop();
                    Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                    number_of_luggage_counters--;
                    event_queue_case_1.push(e);
                }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue.size()){
                Passenger temp = luggage_queue.front();
                luggage_queue.pop();
                event_queue_case_1.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            security_queue.push(current_event.current_passenger);
                if(number_of_security_counters > 0) {
                    Passenger b = security_queue.front();
                    security_queue.pop();
                    Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                    number_of_security_counters--;
                    event_queue_case_1.push(e);
                }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue.size()){
                Passenger temp = security_queue.front();
                security_queue.pop();
                event_queue_case_1.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;


    //case 2:
    TIME = 1;
    missed_flights =0;
    total_minute_passed = 0;

    while(event_queue_case_2.size()){
        Event current_event = event_queue_case_2.top();
        event_queue_case_2.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            luggage_queue_.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue_.top();
                luggage_queue_.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_2.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue_.size()){
                Passenger temp = luggage_queue_.top();
                luggage_queue_.pop();
                event_queue_case_2.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            security_queue_.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue_.top();
                security_queue_.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_2.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue_.size()){
                Passenger temp = security_queue_.top();
                security_queue_.pop();
                event_queue_case_2.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    //case 3:
    TIME = 1;
    missed_flights = 0;
    total_minute_passed = 0;

    while(event_queue_case_3.size()){
        Event current_event = event_queue_case_3.top();
        event_queue_case_3.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            luggage_queue.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue.front();
                luggage_queue.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_3.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue.size()){
                Passenger temp = luggage_queue.front();
                luggage_queue.pop();
                event_queue_case_3.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            if(current_event.current_passenger.is_vip == 'V'){
                total_minute_passed += TIME - current_event.current_passenger.arrival_time;
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            security_queue.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue.front();
                security_queue.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_3.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue.size()){
                Passenger temp = security_queue.front();
                security_queue.pop();
                event_queue_case_3.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }
    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;


    //case 4:
    TIME = 1;
    missed_flights = 0;
    total_minute_passed = 0;

    while(event_queue_case_4.size()){
        Event current_event = event_queue_case_4.top();
        event_queue_case_4.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            luggage_queue_.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue_.top();
                luggage_queue_.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_4.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue_.size()){
                Passenger temp = luggage_queue_.top();
                luggage_queue_.pop();
                event_queue_case_4.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            if(current_event.current_passenger.is_vip == 'V'){
                total_minute_passed += TIME - current_event.current_passenger.arrival_time;
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            security_queue_.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue_.top();
                security_queue_.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_4.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue_.size()){
                Passenger temp = security_queue_.top();
                security_queue_.pop();
                event_queue_case_4.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }
    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    //case 5:
    TIME = 1;
    total_minute_passed = 0;
    missed_flights = 0;

    while(event_queue_case_5.size()){
        Event current_event = event_queue_case_5.top();
        event_queue_case_5.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            if(current_event.current_passenger.is_ocu == 'N'){
                security_queue.push(current_event.current_passenger);
                if(number_of_security_counters > 0){
                    Passenger b = security_queue.front();
                    security_queue.pop();
                    Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                    number_of_security_counters--;
                    event_queue_case_5.push(e);
                }
                continue;
            }
            luggage_queue.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue.front();
                luggage_queue.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_5.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue.size()){
                Passenger temp = luggage_queue.front();
                luggage_queue.pop();
                event_queue_case_5.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            security_queue.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue.front();
                security_queue.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_5.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue.size()){
                Passenger temp = security_queue.front();
                security_queue.pop();
                event_queue_case_5.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    //case 6:
    TIME = 1;
    missed_flights =0;
    total_minute_passed = 0;

    while(event_queue_case_6.size()){
        Event current_event = event_queue_case_6.top();
        event_queue_case_6.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            if(current_event.current_passenger.is_ocu == 'N'){
                security_queue_.push(current_event.current_passenger);
                if(number_of_security_counters > 0){
                    Passenger b = security_queue_.top();
                    security_queue_.pop();
                    Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                    number_of_security_counters--;
                    event_queue_case_6.push(e);
                }
                continue;
            }
            luggage_queue_.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue_.top();
                luggage_queue_.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_6.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue_.size()){
                Passenger temp = luggage_queue_.top();
                luggage_queue_.pop();
                event_queue_case_6.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            security_queue_.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue_.top();
                security_queue_.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_6.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue_.size()){
                Passenger temp = security_queue_.top();
                security_queue_.pop();
                event_queue_case_6.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    //case 7:
    TIME = 1;
    total_minute_passed = 0;
    missed_flights = 0;

    while(event_queue_case_7.size()){
        Event current_event = event_queue_case_7.top();
        event_queue_case_7.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            if(current_event.current_passenger.is_ocu == 'N' && current_event.current_passenger.is_vip == 'V'){
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            if(current_event.current_passenger.is_ocu == 'N'){
                security_queue.push(current_event.current_passenger);
                if(number_of_security_counters > 0){
                    Passenger b = security_queue.front();
                    security_queue.pop();
                    Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                    number_of_security_counters--;
                    event_queue_case_7.push(e);
                }
                continue;
            }
            luggage_queue.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue.front();
                luggage_queue.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_7.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue.size()){
                Passenger temp = luggage_queue.front();
                luggage_queue.pop();
                event_queue_case_7.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            if(current_event.current_passenger.is_vip == 'V'){
                total_minute_passed += TIME - current_event.current_passenger.arrival_time;
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            security_queue.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue.front();
                security_queue.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_7.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue.size()){
                Passenger temp = security_queue.front();
                security_queue.pop();
                event_queue_case_7.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    //case 8:

    TIME = 1;
    total_minute_passed = 0;
    missed_flights = 0;

    while(event_queue_case_8.size()){
        Event current_event = event_queue_case_8.top();
        event_queue_case_8.pop();
        TIME = current_event.time;
        if(current_event.current_type == Event::ARRIVAL){
            if(current_event.current_passenger.is_ocu == 'N' && current_event.current_passenger.is_vip == 'V'){
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            if(current_event.current_passenger.is_ocu == 'N'){
                security_queue_.push(current_event.current_passenger);
                if(number_of_security_counters > 0){
                    Passenger b = security_queue_.top();
                    security_queue_.pop();
                    Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                    number_of_security_counters--;
                    event_queue_case_8.push(e);
                }
                continue;
            }
            luggage_queue_.push(current_event.current_passenger);
            if(number_of_luggage_counters > 0) {
                Passenger a = luggage_queue_.top();
                luggage_queue_.pop();
                Event e = *new Event(TIME+a.luggage_desk_time,a,Event::LUGGAGE_EXIT);
                number_of_luggage_counters--;
                event_queue_case_8.push(e);
            }
        }
        if(current_event.current_type == Event::LUGGAGE_EXIT){
            if(luggage_queue_.size()){
                Passenger temp = luggage_queue_.top();
                luggage_queue_.pop();
                event_queue_case_8.push(*new Event(TIME+temp.luggage_desk_time,temp,Event::LUGGAGE_EXIT));
                number_of_luggage_counters--;
            }
            number_of_luggage_counters++;
            if(current_event.current_passenger.is_vip == 'V'){
                total_minute_passed += TIME - current_event.current_passenger.arrival_time;
                missed_flights += 0 + (TIME > current_event.current_passenger.departure_time);
                continue;
            }
            security_queue_.push(current_event.current_passenger);
            if(number_of_security_counters > 0) {
                Passenger b = security_queue_.top();
                security_queue_.pop();
                Event e = *new Event(TIME + b.security_desk_time,b,Event::SECURITY_EXIT);
                number_of_security_counters--;
                event_queue_case_8.push(e);
            }
        }
        if(current_event.current_type == Event::SECURITY_EXIT){
            if(security_queue_.size()){
                Passenger temp = security_queue_.top();
                security_queue_.pop();
                event_queue_case_8.push(*new Event(TIME+temp.security_desk_time,temp,Event::SECURITY_EXIT));
                number_of_security_counters--;
            }
            number_of_security_counters++;
            total_minute_passed += TIME - current_event.current_passenger.arrival_time;
            if(TIME > current_event.current_passenger.departure_time){
                missed_flights++;
            }
        }
    }

    cout << (total_minute_passed*1.0/number_of_passengers) << " " << missed_flights << endl;

    return 0;
}