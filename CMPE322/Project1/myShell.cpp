#include <string>
#include <vector>
#include <istream>
#include <sstream>
#include <fcntl.h>
#include <iostream>
#include <iterator>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <algorithm>
#include <sys/wait.h>
#include <sys/types.h>

#define PROMPT " >>> "
#define INPUT 0
#define OUTPUT 1

using namespace std;

int historyCount = 0; // It is the global index of the command whether it is in the history vector or not, implemented due to the inspration of Linux.

string prepConfig();

vector<string> lineBreaker(string line);

bool validCommand(string command);

void printHistory(vector<string>* history);

void setHistory(vector<string>* history, vector<string> broken);

vector<vector<string>> commander(vector<string> broken);

int createSinglePhaseProcess(vector<string> singleCommand);

void createPipeProcess(vector<vector<string>> commandList);

int main(){
    string line;
    vector<string> brokenline; // tokenized input line
    vector<string> history(15); // a vector that holds the history
    vector<vector<string>> commandList; // list of commands that holds the input.

    while(1){
        cout << prepConfig(); // creates the prompt
        getline(cin, line);
        
        if(line == "exit"){ // check for 'exit' command
            return 0;
        }
        if(line == ""){ // check for return
            continue;
        }
        
        brokenline = lineBreaker(line); // tokenize the line
        setHistory(&history, brokenline); // adds the command in history
        
        if(line == "footprint"){ // checks for history command
            printHistory(&history); // prints the current history
            continue;
        }
        commandList = commander(brokenline); // removes pipes and redirections and prepares the actual input
        
        if(validCommand(commandList[0][0])){ // check for first command whether it is valid or not. (e.g. >>> listdir -a)
            if(commandList.size() == 1){ // checks for total command whether it's one command or more.
                createSinglePhaseProcess(commandList[0]); // creates one command process
            }
            else {
                createPipeProcess(commandList); // creates one piped commands
            }
        }
    }
}

string prepConfig(){
    /*
        returns the username and the prompt delimiter.
    */
    return (string)getenv("USERNAME") + PROMPT;
}

vector<string> lineBreaker(string line){
    /*
        splits the input string 'line' via spaces, and checks if there's any concatenated arguments. (e.g. listdir -a|grep .)
        if so, then splits the concatenation and adds the related tokens into vector, namely brokenFinal.
    */
    vector<string> brokenFinal;
    istringstream iss(line);
    vector<string> broken(istream_iterator<string>{iss}, istream_iterator<string>());

    for(string s: broken){
        if(s != "|" && s != ">"){
            if(s.find("\"") != string::npos){
                string quoteTrimmed = s.substr(1, s.length() - 2);
                brokenFinal.push_back(quoteTrimmed);
            }
            string complexToken = s;
            string fragment;

            auto pipeIndex = complexToken.find("|"); // check if there's any pipe in token. "find() returns first seen index of delimiter."
            auto writeIndex = complexToken.find(">"); // check if there's any redirection in token. "find() returns first seen index of delimiter."
        
            if(pipeIndex != string::npos){  // if seen, split the token into subtokens and add.
                fragment = complexToken.substr(0, pipeIndex);
                complexToken = complexToken.substr(pipeIndex + 1, complexToken.length());
                brokenFinal.push_back(fragment);
                brokenFinal.push_back("|");
                brokenFinal.push_back(complexToken);
            }
            else{
                if(writeIndex != string::npos){ // if seen, split the token int subtokens and add.
                    fragment = complexToken.substr(0, writeIndex);
                    complexToken = complexToken.substr(writeIndex + 1, complexToken.length());
                    brokenFinal.push_back(fragment);
                    brokenFinal.push_back(">");
                    brokenFinal.push_back(complexToken);
                }
                else{
                brokenFinal.push_back(complexToken);
                }
            }
        }
        else {
            brokenFinal.push_back(s);
        }
    }

    return brokenFinal;
}

bool validCommand(string command){
    /*
        checks for any command whether it is valid or not. Valid commands are given as valid() = {listdir, currentpath, footprint, printfile, grep}
    */
    vector<string> commands = {"listdir", "currentpath", "footprint", "printfile", "grep", "overwrite"};
    for(string s: commands){
        if(s == command){
            return true;
        }
    }
    return false;
}

string concat(vector<string> broken){
    /*
        String concatenator for utility needs.
    */
    string merged;
    for(string s: broken){
        merged += s + " ";
    }
    return merged.substr(0, merged.length() - 1);
}

void printHistory(vector<string>* history){
    /*
        prints the history vector to stdout with the index numbers before the commands.
    */
    int historySize = (*(history)).size(); // size of the vector

    for(int i = 0; i < historySize; i++){
        if((*(history))[i] != "") {
            cout << (historyCount - historySize + i + 1) << "\t" << (*(history))[i] << endl;
        }
    }

}

void setHistory(vector<string>* history, vector<string> broken){
    /*
        Adds the current command typed into stdin and checks if it is same as the former command. 
        If so, it doesn't add the current command into history, same as Linux approach.
    */
    if((*(history)).size() == 0){
        (*(history)).push_back(concat(broken));
        historyCount++;
    }
    else {
        string merged = concat(broken); // concatenates the broken command tokens.
        if((*(history)).back() != merged){
            if((*(history)).size() == 15){ // check for the size, given in the project description.
                (*(history)).erase((*(history)).begin());
            }
            (*(history)).push_back(merged);
            historyCount++;
        }
    }
}

vector<vector<string>> commander(vector<string> broken){
    /*
        It is the parser for subcommands given in a line of command, meaning as 'pipe' and redirections.
        Checks for any sign of those delimiters and formats the input command to more structural format.
        (e.g.) listdir -a | grep . ==> [listdir, -a, |, grep, .] ==> [[listdir, -a], [grep, .]]
    */
    vector<vector<string>> commandList;
    vector<string> commandArgs;

    for(int it_1 = 0; it_1 < broken.size(); it_1++){
        if(broken[it_1] == "|"){ // if pipe, then split the command and start the next phase of the overall process.
            commandList.push_back(commandArgs);
            commandArgs.clear();
        }else if(broken[it_1] == ">"){ // same as pipe, '>' version. (redirection symbol is formatted as "overwrite.") 
            commandList.push_back(commandArgs);
            commandArgs.clear();
            commandArgs.push_back("overwrite");
        }else {
            commandArgs.push_back(broken[it_1]);
        }
    }

    if(commandArgs.size() != 0){ // puts the last part into the total process matrix(2D string vector).
        commandList.push_back(commandArgs);
        commandArgs.clear();
    }

    return commandList;
}

int createSinglePhaseProcess(vector<string> singleCommand){
    /*
        Creates single phase process. Uses fork/exec combination for that.
        Inputs are hard coded for simplicity.
        The genuine version of this shell will be uploaded to https://www.github.com/oztasozgurcan/myShell
    */    
    pid_t pid;

    pid = fork();

    if(pid < 0){
        fprintf(stderr, "Fork Failed.");
        return 1;
    } else if(pid == 0){
        if(singleCommand[0] == "listdir"){
            if(singleCommand.size() > 1){
                execlp("ls", "ls", "-a", NULL);
                return 0;
            } else {
                execlp("ls", "ls", NULL);
                return 0;
            }
        }
        else if(singleCommand[0] == "printfile"){
            /*
                String to char array converter, stable version. Used in many places, very much redundancy can be seen.
                Redundancy will be removed.
            */
            string file = singleCommand[1];
            int filesize = file.size();
            char filename[filesize];
            strcpy(filename, file.c_str());
            execlp("cat", "cat", filename, NULL);
        }
        else {
            execlp("pwd", "pwd", NULL);
            return 0;
        }
        
    } else {
        wait(NULL); // wait for input command which gets executed.
        return 0;
    }

}

void createPipeProcess(vector<vector<string>> commandList){
    /*
        Creates two or more phase piped or redirected processes given into one command line.
        Commands are hardcoded, for the sake of the simplicity of the project.
        Redundancy can be seen as string to char array converter. Sorry for that.
        Next update will not have such bad coding signs.  
    */
    if(commandList.size() == 2){
        pid_t pid;
        if(!validCommand(commandList[1][0])){
            return;
        }
        pid = fork();

        if(pid < 0){
            fprintf(stderr, "Fork Failed.");
        } else if(pid == 0){
            if(commandList[1][0] == "overwrite"){ // checks for redirection
                if(commandList[0][0] == "printfile"){ // checks for the combination of "printfile a.txt > b.txt"
                    string file = commandList[0][1];
                    string dest = commandList[1][1];
                    
                    int fileWidth = file.size();
                    int destWidth = dest.size();
                    
                    char filename[fileWidth];
                    char destname[destWidth];

                    strcpy(filename, file.c_str());
                    strcpy(destname, dest.c_str());

                    int fd = open(destname, O_WRONLY | O_CREAT, 0666); // file descriptor of the process.
                    dup2(fd, OUTPUT);

                    execlp("cat", "cat", filename, NULL);
                }
            }
            else if(commandList[1][0] == "grep"){ // checks for pipe
                pid_t pid2;
                int gateways[2], gw;
                gw = pipe(gateways); // open pipe
                if(gw < 0){
                    perror("Pipe failed.");
                    exit(EXIT_FAILURE);
                }

                pid2 = fork(); // forks for the piped subcommand

                if(pid2 == 0){ // child side of the fork
                    close(gateways[INPUT]); // closes input ends of pipe for child
                    dup2(gateways[OUTPUT], OUTPUT); // copies output end for child
                    close(gateways[INPUT]);
                    if(commandList[0].size() == 1){ // check for listdir (e.g. listdir | grep .)
                        execlp("ls", "ls", NULL);
                    }
                    else { // check for listdir -a (e.g. listdir -a | grep .)
                        execlp("ls", "ls", "-a", NULL);
                    }
                }
                else { // parent side of the fork
                    close(gateways[OUTPUT]); // closes output ends of pipe for parent.
                    dup2(gateways[INPUT], INPUT); // copies input end for parent
                    close(gateways[OUTPUT]);
                    wait(NULL);
                    string pattern = commandList[1][1];
                    int patternlen = pattern.size();
                    char patt[patternlen];
                    strcpy(patt, pattern.c_str());
                    execlp("grep", "grep", patt ,NULL); // executes grep in parent with the redirected output of its child.
                }
            }
        }
        else {
            wait(NULL); // wait for the input command which gets executed.
        }
    }
}