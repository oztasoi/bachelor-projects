#include <stdio.h>
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

int general_index = 0;
int bunch_id = 0;
int number_of_broken_boxes;

class Money_Box{
public:
    int id;
    int number_of_edges = 0;
    int index = -1;
    int group_id;
    int lowlink;
    bool onstack = false;
    vector<int> edge_list;

    Money_Box(int _id){
        this->id = _id;
    }

    void insert_edge(int m){
        this->edge_list.push_back(m);
        this->number_of_edges++;
    }
};

class Graph{
public:

    int number_of_vertices;
    vector<Money_Box> vertex_list;

    Graph(int _number_of_vertices){
        this->number_of_vertices = _number_of_vertices;
    }
};

class Bunch_of_Money_Box{
public:
    int id;
    bool is_breakable = true;
    vector<Money_Box> current_cycle;

    Bunch_of_Money_Box(int _id){
        this->id = _id;
    }
};

void dfs_traversal(Graph& g, stack<Money_Box>& current_stack,
         Money_Box& current_box,vector<Bunch_of_Money_Box> current_cycles){
    current_box.index = general_index;
    current_box.lowlink = general_index;
    general_index = general_index +1;
    current_stack.push(current_box);
    current_box.onstack = true;

    for(int i=0;i<current_box.edge_list.size();i++){
        Money_Box temp = g.vertex_list[current_box.edge_list[i]];
        if(temp.index == -1){
            dfs_traversal(g,current_stack,temp,current_cycles);
            current_box.lowlink = min(current_box.lowlink,temp.lowlink);
        }
        else if(temp.onstack){
            current_box.lowlink = min(current_box.lowlink,temp.index);
        }
    }

    if(current_box.lowlink == current_box.index){
        Bunch_of_Money_Box current_bunch(bunch_id);
        int temp_box_id;
        do{
            Money_Box temp = current_stack.top();
            current_stack.pop();
            temp_box_id = temp.id;
            temp.group_id = bunch_id;
            current_bunch.current_cycle.push_back(temp);

        }while(current_box.id != temp_box_id);
        current_cycles.push_back(current_bunch);
        bunch_id++;
    }
}

void find_scc(Graph& g, stack<Money_Box>& current_stack, vector<Bunch_of_Money_Box>& current_cycles){
    for(int i=0;i<g.number_of_vertices;i++){
        if(g.vertex_list[i].index == -1){
            dfs_traversal(g,current_stack,g.vertex_list[i],current_cycles);
        }
    }
}


int main(int argc, char* argv[]){

    freopen(argv[1],"r",stdin);

    int number_of_vertices;
    scanf("%d",&number_of_vertices);

    Graph current_graph(number_of_vertices);

    for(int i=0;i<number_of_vertices;i++){
        int number_of_keys;
        scanf("%d",&number_of_keys);

        Money_Box current_box(i+1);
        for(int j=0;j<number_of_keys;j++){
            int current_key;
            scanf("%d", &current_key);
            current_box.edge_list.push_back(current_key);
        }

        current_graph.vertex_list.push_back(current_box);
    }

    stack<Money_Box> my_stack;
    vector<Bunch_of_Money_Box> current_cycles;
    find_scc(current_graph,my_stack,current_cycles);

    number_of_broken_boxes = current_cycles.size();

    for(int i=0;i<current_graph.number_of_vertices;i++){
        Money_Box current_box = current_graph.vertex_list[i];
        for(int j=0;j<current_box.number_of_edges;j++){
            int target_group_id = current_graph.vertex_list[current_box.edge_list[j]].group_id;
            if(target_group_id != current_box.group_id){
                current_cycles[target_group_id-1].is_breakable = false;
                number_of_broken_boxes--;
            }
        }
    }

    cout << number_of_broken_boxes << endl;

    for(int i=0;i<current_cycles.size();i++){
        if(current_cycles[i].is_breakable){
            cout << current_cycles[i].current_cycle[0].id << " " << endl;
        }
    }

    return 0;
}