#include <vector>
#include <set>
#include <iostream>

using namespace std;

vector<vector<int>> grid;
vector<vector<int>> min_dif;

class Vertex{
public:
    int x,y;
    int height;

    Vertex(int ax,int ay){
        this->x = ax;
        this->y = ay;
    }

    Vertex(int ax, int ay, int aheight){
        this->x = ax;
        this->y = ay;
        this->height = aheight;
    }

    static bool is_inside(int x,int y,int row, int column){
        return x >= 0 && x < row && y >= 0 && y < column;
    }
};

struct Compare_Vertex{

    bool operator()(const Vertex &v1, const Vertex &v2){

        if(v1.height == v2.height){
            if(v1.x == v2.x){
                return v1.y < v2.y;
            }
            return v1.x < v2.x;
        }
        return v1.height < v2.height;
    }
};

int mst(int row, int column,int x1, int y1, int x2, int y2){

    int hn[] = {-1,0,1,0};
    int vn[] = {0,1,0,-1};

    min_dif[x1][y1] = 0;

    Vertex source = *new Vertex(x1,y1);
    set<Vertex,Compare_Vertex> vertex_set;
    vertex_set.insert(source);

    while(!vertex_set.empty()){
        Vertex cur = *vertex_set.begin();
        vertex_set.erase(vertex_set.begin());

        if(cur.x == x2 && cur.y == y2){
            return min_dif[cur.x][cur.y];
        }

        for(int i=0;i<4;i++){

            int x = cur.x + hn[i];
            int y = cur.y + vn[i];

            if(!Vertex::is_inside(x,y,row,column))
                continue;

            if(min_dif[x][y] > max(min_dif[cur.x][cur.y], abs(grid[x][y]-grid[cur.x][cur.y]))){

                if(min_dif[x][y] != INT32_MAX && x != x2 && y != y2){
                    vertex_set.erase(vertex_set.find(Vertex(x,y,min_dif[x][y])));
                }

                min_dif[x][y] = max(min_dif[cur.x][cur.y], abs(grid[x][y]-grid[cur.x][cur.y]));
                vertex_set.insert(*new Vertex(x,y,min_dif[x][y]));
            }
        }
    }

}

int main(int argc,char* argv[]){

    if(argc != 3){
        return 1;
    }

    freopen(argv[1],"r",stdin);
    freopen(argv[2],"w+",stdout);

    int row, column;
    scanf("%d %d",&row,&column);
    grid.resize(row);
    min_dif.resize(column);

    for(int i=0;i<row;i++){
        grid[i].resize(column);
        min_dif[i].resize(column);
        for(int j=0;j<column;j++){
            int current_height;
            scanf("%d",&current_height);
            grid[i][j] = current_height;
            min_dif[i][j] = INT32_MAX;
        }
    }

    int query;
    scanf("%d",&query);

    for(int i=0;i<query;i++){
        int x1,y1,x2,y2;
        scanf("%d %d %d %d", &x1,&y1,&x2,&y2);
        int ladder = mst(row,column,(x1-1),(y1-1),(x2-1),(y2-1));
        printf("%d\n", ladder);
    }
}