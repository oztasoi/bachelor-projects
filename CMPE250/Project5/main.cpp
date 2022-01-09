#include <iostream>
#include <set>
#include <fstream>
#include <vector>

int mod = 1000000007;
int alphabet = 256;
int reprime = 101;

using namespace std;
vector<vector<int>> occurence_matrix(1001,vector<int>(1,0));
long long int memoize[1001] = {};

void search(string pat, string txt)
{
    int M = pat.length();
    int N = txt.length();
    int i, j;
    int p = 0;
    int t = 0;
    int h = 1;

    for (i = 0; i < M-1; i++)
        h = (h*alphabet)%reprime;
    for (i = 0; i < M; i++) {
        p = (alphabet*p + pat[i])%reprime;
        t = (alphabet*t + txt[i])%reprime;
    }
    for (i = 0; i <= N - M; i++) {
        if ( p == t )
        {
            for (j = 0; j < M; j++) {
                if (txt[i+j] != pat[j])
                    break;
            }
            if (j == M) {
                occurence_matrix[i].push_back(M);
            }
        }
        if ( i < N-M ) {
            t = (alphabet*(t - txt[i]*h) + txt[i+M])%reprime;
            if (t < 0)
                t = (t + reprime);
        }
    }
}

int main(int argc, char* argv[]){

    if(argc != 3){
        return 1;
    }

    ifstream ifs;
    ofstream ofs;

    ifs.open(argv[1]);
    ofs.open(argv[2]);

    string message;
    ifs >> message;

    int dictionary_size;
    ifs >> dictionary_size;

    while(!ifs.eof()){
        string current;
        ifs >> current;
        search(current,message);
    }

    memoize[0] = 1;

    int message_index, current_iterator;
    message_index = 1; current_iterator = 0;

    while(message_index < message.size()+1){
        while(current_iterator < occurence_matrix[message_index-1].size()){
            if(occurence_matrix[message_index-1][current_iterator] != 0) {
                memoize[message_index + occurence_matrix[message_index - 1][current_iterator] - 1] =
                        (memoize[message_index + occurence_matrix[message_index - 1][current_iterator] - 1] + memoize[message_index - 1]) % mod;
            }
            current_iterator++;
        }
        current_iterator=0;
        message_index++;
    }

    ofs << memoize[message.size()] << endl;
    return 0;
}
