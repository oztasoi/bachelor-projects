// Name: Ibrahim Ozgurcan Oztas
// Student ID: 2016400198
// Compile Status: Compiling
// Runtime Status: Working

#include <mpi.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>

using namespace std;

class Sliceable {
    
    private:
    char *infile;
    char *outfile;

    public:
    int grid[360][360];
    Sliceable(){
        infile = nullptr;
        outfile = nullptr;
    }

    static int convert(char c){
        return c - 48;
    }

    void setInfile(char *in){
        this->infile = in;
    }

    char* getInfile(){
        return this->infile;
    }

    void setOutfile(char *out){
        this->outfile = out;
    }

    char* getOutfile(){
        return this->outfile;
    }

    void setGrid(){
        ifstream ifs(infile, ifstream::in);
        
        int rowPosition, columnPosition;
        rowPosition = 0; columnPosition = 0;
        char c;
        
        do{
            if(columnPosition == 360){
                ifs.clear();
                rowPosition++;
                columnPosition = 0;
            }

            c = ifs.get();

            if(c == 48 || c == 49){
                this->grid[rowPosition][columnPosition] = Sliceable::convert(c);
                columnPosition++;
            }
            else {
                continue;
            }
        }
        while(!ifs.eof());
    }

    void writeGrid(){
        ofstream ofs(outfile, ofstream::out);
        for(int i=0; i<360; i++){
            for(int j=0; j<360; j++){
                ofs << this->grid[i][j] << " ";
            }
            ofs << "\n";
            ofs.flush();
        }
        ofs.close();
    }
};

int main(int argc, char *argv[]){
    // The solution is based on periodic approach with checkered positioned slave processes.

    if(argc != 4){
        printf("Invalid amount of parameters. Aborted\n");
    }
    
    int err, processor, rank;

    err = MPI_Init(&argc, &argv);
    err = MPI_Comm_size(MPI_COMM_WORLD, &processor);
    err = MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if(rank == 0){
        int check = (int)sqrt(processor - 1);
        int slaveX = 360 / check;
        MPI_Status status;

        Sliceable *toroid = new Sliceable();
        (*toroid).setInfile(argv[1]);
        (*toroid).setOutfile(argv[2]);

        (*toroid).setGrid();
        /*
        - I split the grid into (p-1) subgrids to distribute in slave processes.
        - And for ease of use, I send the frame that surrounds each subgrid.
        - e.g. if subgrid has n*n matrix, I send (n+2)*(n+2) to slave processes to execute first iteration without any intercommunication.
        - Since grid is in a shape of toroid, for border cases there has to be a connection between borders and their neighbours on toroid. Since toroid connects borders periodically, I put modulus to avoid reaching out invalid index on grid.
            - e.g. if i = -1: since there's no -1 index on grid, it should be 360 - 1 = 359.

        Variables 'latitude' and 'longitude' represent location of each element inside the grid, based on the process rank. Each process will receive its own subgrid data depending on its rank.

        e.g. For p = 5;
        
        | 1 0 1 0 |
        | 1 0 0 1 |
        | 0 0 0 1 |
        | 1 1 0 0 |
        
        This grid will divide into four subgrids:
        p == 1 => [[1, 0], [1, 0]]; latitude = (((1-1)/2)*(4/2))-1 = -1; 
                                    longitude = (((1-1)%2)*(4/2))-1 = -1;
        p == 2 => [[1, 0], [0, 1]]; latitude = (((2-1)/2)*(4/2))-1 = -1;
                                    longitude = (((2-1)%2)*(4/2))-1 = 1;
        p == 3 => [[0, 0], [1, 1]]; latitude = (((3-1)/2)*(4/2))-1 = 1;
                                    longitude = (((3-1)%2)*(4/2))-1 = -1;
        p == 4 => [[0, 1], [0, 0]]; latitude = (((4-1)/2)*(4/2))-1 = 1;
                                    longitude = (((4-1)%2)*(4/2))-1 = 1;
        Those values are starting indexes for each process's subgrid. 
        Master process send data to slave processes related to their subgrid.

        - 'check' is the dimension of checker board. 
            ==> processor = check * check + 1;
                - '+1' for the master process.
        - 'slaveX' is the dimension of each process's subgrid.
            ==> slaveX = (int)sqrt(processor - 1); 
                - In project, we have precise dimensions, 360*360. Hence,
                - e.g. For p = 17, check = 4, slaveX = 90.
                - e.g. For p = 65, check = 8, slaveX = 45.
                - e.g. For p = 145, check = 12, slaveX = 30.
        */

        int latitude, longitude;
        for(int p=1; p<processor; p++){
            latitude = (((p-1)/check)*slaveX);
            longitude = (((p-1)%check)*slaveX);
            for(int i=latitude-1; i<latitude+slaveX+1; i++){
                for(int j=longitude-1; j<longitude+slaveX+1; j++){
                    err = MPI_Send(&toroid->grid[(i+360)%360][(j+360)%360], 1, MPI_INT, p, p, MPI_COMM_WORLD);
                }
            }
        }

        /*
        I retrieve data from slave processes based on the tag. Each slave send its tag while sending data to master, hence data is not shuffled among slaves while master is retrieving data.
        */

        for(int p=1; p<processor; p++){
            for(int i=(((p-1)/check)*slaveX); i<((((p-1)/check)+1)*slaveX); i++){
                for(int j=(((p-1)%check)*slaveX); j<((((p-1)%check)+1)*slaveX); j++){
                    err = MPI_Recv(&toroid->grid[i][j], 1, MPI_INT, p, p, MPI_COMM_WORLD, &status);
                }
            }
        }

        /*
        Call write-to-file method of class Sliceable.
        */

        (*toroid).writeGrid();
        
        MPI_Finalize();
    }
    else {
        int check = (int)sqrt(processor - 1);
        int size = (360 / check) + 2;
        // int arr[size*size];
        // Previous state of iteration.
        int before[size][size];
        // Next state after iteration.
        int after[size-2][size-2];
        MPI_Status status;

        for(int i=0; i<size; i++){
            for(int j=0; j<size; j++){
               err = MPI_Recv(&before[i][j], 1, MPI_INT, 0, rank, MPI_COMM_WORLD, &status);
            }
        }

        // for(int i=0; i<size; i++){
        //     for(int j=0; j<size; j++){
        //         before[i][j] = arr[size*i+j];
        //     }
        // }
        
        int iterations = stoi(argv[3]);
        for(int turn=0; turn<iterations; turn++){
            for(int i=1; i<size-1; i++){
                for(int j=1; j<size-1; j++){
                    
                    int env_resources = (before[i-1][j-1] + before[i][j-1] + before[i+1][j-1] + before[i-1][j] + before[i+1][j] + before[i-1][j+1] + before[i][j+1] + before[i+1][j+1]);

                    if(before[i][j] == 1){
                        if(env_resources < 2){
                            after[i-1][j-1] = 0;
                        }
                        else if(env_resources > 3){
                            after[i-1][j-1] = 0;
                        }
                        else
                        {
                            after[i-1][j-1] = 1;
                        }
                    }
                    else
                    {
                        if(env_resources == 3){
                            after[i-1][j-1] = 1;
                        }
                        else
                        {
                            after[i-1][j-1] = 0;
                        }
                    }
                }
            }

            // After iterations, put the current state data to previous state grid.
            // To be used in next iteration.
            for(int i=1; i<size-1; i++){
                for(int j=1; j<size-1; j++){
                    before[i][j] = after[i-1][j-1];
                }
            }
            // After then, communication begins. Each case is explicitly written below.
            // It can be rearranged into generic if cases, since the communication tags are distinctive.

            // Odd Sends the right column
            if(rank%2==1){
                for(int i=0; i<size-2;i++){
                    err = MPI_Send(&after[i][size-3], 1, MPI_INT, rank+1, 1, MPI_COMM_WORLD);
                }
            }
            
            // Even Receives the left column.
            if(rank%2==0){
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[i+1][0], 1, MPI_INT, rank-1, 1, MPI_COMM_WORLD, &status);
                }
            }

            // Odd Sends the left column.
            if(rank%2==1){
                int dest = rank - 1;
                // If the letfmost edge sent, map it to its right receiver.
                if(dest%check == 0){
                    dest = dest + check;
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[i][0], 1, MPI_INT, dest, 2, MPI_COMM_WORLD);
                }
            }

            // Even Receives the right column.
            if(rank%2==0){
                int dest = rank + 1;
                // If the rightmost edge receives, map it to its right sender.
                if(dest % check == 1){
                    dest = dest - check;
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[i+1][size-1], 1, MPI_INT, dest, 2, MPI_COMM_WORLD, &status);
                }
            }

            // Even Sends the left column.
            if(rank%2==0){
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[i][0], 1, MPI_INT, rank-1, 3, MPI_COMM_WORLD);
                }
            }

            // Odd Receives the right column.
            if(rank%2==1){
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[i+1][size-1], 1, MPI_INT, rank+1, 3, MPI_COMM_WORLD, &status);
                }
            }

            // Even Sends the right column.
            if(rank%2==0){
                int dest = rank + 1;
                // If the righmost edge sent, map it to its right receiver.
                if(dest%check==1){
                    dest = dest - check;
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[i][size-3], 1, MPI_INT, dest, 4, MPI_COMM_WORLD);
                }
            }

            // Odd Receives the left column.
            if(rank%2==1){
                int dest = rank - 1;
                // If the leftmost edge receives, map it to its right sender.
                if(dest%check==0){
                    dest = dest + check;
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[i+1][0], 1, MPI_INT, dest, 4, MPI_COMM_WORLD, &status);
                }
            }

            // Odd Sends the bottom row.
            if(((rank-1)/check)%2==1){
                int dest = rank + check;
                // If the destination is bigger than number of slaves, remap it to the right receiver.
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[size-3][i], 1, MPI_INT, dest, 1, MPI_COMM_WORLD);
                }
            }

            // Even Receives the top row.
            if(((rank-1)/check)%2==0){
                int dest = rank - check;
                // If the destination is less than 1, which is either master or does not exist, remap it to the right sender.
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[0][i+1], 1, MPI_INT, dest, 1, MPI_COMM_WORLD, &status);
                }
            }

            // Odd Sends the top row.
            if(((rank-1)/check)%2==1){
                int dest = rank - check;
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[0][i], 1, MPI_INT, dest, 2, MPI_COMM_WORLD);
                }
            }

            // Even Receives the bottow row.
            if(((rank-1)/check)%2==0){
                int dest = rank + check;
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[size-1][i+1], 1, MPI_INT, dest, 2, MPI_COMM_WORLD, &status);
                }
            }

            // Even Sends the bottom row.
            if(((rank-1)/check)%2==0){
                int dest = rank + check;
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[size-3][i], 1, MPI_INT, dest, 3, MPI_COMM_WORLD);
                }
            }

            // Odd Receives the top row.
            if(((rank-1)/check)%2==1){
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[0][i+1], 1, MPI_INT, rank-check, 3, MPI_COMM_WORLD, &status);
                }
            }

            // Even Sends the top row.
            if(((rank-1)/check)%2==0){
                int dest = rank - check;
                // If the destination is less than 1, which is either master or does not exist, remap it to the right receiver.
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Send(&after[0][i], 1, MPI_INT, dest, 4, MPI_COMM_WORLD);
                }
            }

            // Odd Receives the bottom row.
            if(((rank-1)/check)%2==1){
                int dest = rank + check;
                // If the destination is greater than number of slaves, remap it to the right sender.
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                for(int i=0; i<size-2; i++){
                    err = MPI_Recv(&before[size-1][i+1], 1, MPI_INT, dest, 4, MPI_COMM_WORLD, &status);
                }
            }
            // TODO: Add diagonals.
            // Odd Sends the bottomright.
            if(rank%2==1){
                int dest = rank + (check + 1);
                // If the destination is greater than number of slaves, remap it to the right receiver.
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Send(&after[size-3][size-3], 1, MPI_INT, dest, 1, MPI_COMM_WORLD);
            }

            // Even Receives the topleft.
            if(rank%2==0){
                int dest = rank - (check + 1);
                // If the destination is less than 1, which is either master or does not exist, remap it to the right receiver.
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[0][0], 1, MPI_INT, dest, 1, MPI_COMM_WORLD, &status);
            }

            // Odd Sends the bottomleft.
            if(rank%2==1){
                int dest = rank + (check - 1);
                // If the leftmost edge corner sent, remap it to its right receiver.
                if(rank%check==1){
                    dest = dest + check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Send(&after[size-3][0], 1, MPI_INT, dest, 2, MPI_COMM_WORLD);
            }

            // Even Receives the topright.
            if(rank%2==0){
                int dest = rank - (check - 1);
                // If the rightmost upper edge corner received, remap it to its right sender.
                if(rank%check==0){
                    dest = dest - check;
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[0][size-1], 1, MPI_INT, dest, 2, MPI_COMM_WORLD, &status);
            }

            // Odd Sends the topleft.
            if(rank%2==1){
                int dest = rank - (check + 1);
                // If the leftmost upper edge corner is sent, remap it when it was sent from leftmost slaves.
                if(rank%check==1){
                    dest = dest + check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Send(&after[0][0], 1, MPI_INT, dest, 3, MPI_COMM_WORLD);
            }

            // Even Receives the bottomright.
            if(rank%2==0){
                int dest = rank + (check + 1);
                // If the rightmost lower edge corner is received, remap it when it was sent from leftmost upper slaves.
                if(rank%check==0){
                    dest = dest - check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[size-1][size-1], 1, MPI_INT, dest, 3, MPI_COMM_WORLD, &status);
            }

            // Odd Sends the topright.
            if(rank%2==1){
                int dest = rank - (check - 1);
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Send(&after[0][size-3], 1, MPI_INT, dest, 4, MPI_COMM_WORLD);
            }

            // Even Receives the bottomleft.
            if(rank%2==0){
                int dest = rank + (check - 1);
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Recv(&before[size-1][0], 1, MPI_INT, dest, 4, MPI_COMM_WORLD, &status);
            }

            // Even Sends the bottomleft.
            if(rank%2==0){
                int dest = rank + (check - 1);
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Send(&after[size-3][0], 1, MPI_INT, dest, 1, MPI_COMM_WORLD);
            }

            // Odd Receives the topright.
            if(rank%2==1){
                int dest = rank - (check - 1);
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[0][size-1], 1, MPI_INT, dest, 1, MPI_COMM_WORLD, &status);
            }

            // Even Sends the bottomright.
            if(rank%2==0){
                int dest = rank + (check + 1);
                if(rank%check == 0){
                    dest = dest - check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Send(&after[size-3][size-3], 1, MPI_INT, dest, 2, MPI_COMM_WORLD);
            }

            // Odd Receives the topleft.
            if(rank%2==1){
                int dest = rank - (check + 1);
                if(rank%check==1){
                    dest = dest + check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[0][0], 1, MPI_INT, dest, 2, MPI_COMM_WORLD, &status);
            }

            // Even Sends the topleft.
            if(rank%2==0){
                int dest = rank - (check + 1);
                if(dest < 0){
                    dest = dest + (processor - 1);
                }
                err = MPI_Send(&after[0][0], 1, MPI_INT, dest, 3, MPI_COMM_WORLD);
            }

            // Odd Receives the bottomright.
            if(rank%2==1){
                int dest = rank + (check + 1);
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Recv(&before[size-1][size-1], 1, MPI_INT, dest, 3, MPI_COMM_WORLD, &status);
            }

            // Even Sends the topright.
            if(rank%2==0){
                int dest = rank - (check - 1);
                if(rank%check==0){
                    dest = dest - check;
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                err = MPI_Send(&after[0][size-3], 1, MPI_INT, dest, 4, MPI_COMM_WORLD);
            }

            // Odd Receives the bottomleft.
            if(rank%2==1){
                int dest = rank + (check - 1);
                if(rank%check==1){
                    dest = dest + check;
                }
                if(dest > (processor - 1)){
                    dest = dest - (processor - 1);
                }
                if(dest < 1){
                    dest = dest + (processor - 1);
                }
                err = MPI_Recv(&before[size-1][0], 1, MPI_INT, dest, 4, MPI_COMM_WORLD, &status);
            }
        }

        // Sends the information to the master.
        // If there's no iteration, the previous state will be output.
        // Else, the result grid of iterations will be sent.
        if(iterations == 0){
            for(int i=0; i<size-2; i++){
                for(int j=0; j<size-2; j++){
                    err = MPI_Send(&before[i+1][j+1], 1, MPI_INT, 0, rank, MPI_COMM_WORLD);
                }
            }
        }
        else {
            for(int i=0; i<size-2; i++){
                for(int j=0; j<size-2; j++){
                    err = MPI_Send(&after[i][j], 1, MPI_INT, 0, rank, MPI_COMM_WORLD);
                }
            }
        }
        
        err = MPI_Finalize();
    }
}