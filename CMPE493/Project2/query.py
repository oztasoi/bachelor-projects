import sys
import copy
import json
import signal

from constants import REUTERS_DIR

def query_parser(query):
    cleanQuery = query.strip()
    if cleanQuery[-1] == "*":
        return cleanQuery[:-1], True
    else:
        return cleanQuery, False

def wordHuntByPrefix(_prefix):
    wordList = [] # all words starting with a prefix `_prefix`
    prefixStack = [] # stack to execute depth first search to traverse all nodes in trie
    currentPos = trie # current position as root of trie

    for char in _prefix:
        currentPos = currentPos[char] # iterate the current position to the position of the prefix

    # if prefix is already a product of a leaf node, return itself
    if currentPos == {}:
        wordList.append(_prefix)
        return wordList

    # append current prefix and its descendants into the stack
    prefixStack.append((_prefix, currentPos))

    # execute depth first search iteratively.
    while True:
        if len(prefixStack) == 0: # if stack is empty, finish the search
            break
        else:
            prefix, prefix_obj = prefixStack.pop() # pops the last element that has been appended to stack
            for char in prefix_obj.keys(): # check its keys to get the next words
                prefix_copy_obj = copy.deepcopy(prefix_obj) # copies the current position
                new_prefix_obj = prefix_copy_obj[char] # sets the new position
                new_prefix = prefix + char # sets the new prefix
                wordList.append(new_prefix) # adds the prefix in the wordlist
                prefixStack.append((new_prefix, new_prefix_obj)) # appends the new position to the stack to get processed

    return wordList


def docIdHuntByWord(_word):
    if _word not in inv_dict.keys():
        print("{} does not occur in the data set.".format(_word))
        return
    docIdList = inv_dict[_word]
    docIdsList = [docId for docId in docIdList.keys()]
    freqList = [docIdList[docId] for docId in docIdList.keys()]
    
    print("--> `{}` has been found {} times in the following articles:".format(_word, sum(freqList)))
    print("--> Article IDs:\n{}".format(docIdsList))

def query_handler(_query):
    if _query == "###":
        sys.exit(0)
    cleanQuery, isPrefix = query_parser(_query)
    if isPrefix:
        wordList = wordHuntByPrefix(cleanQuery)
        for word in wordList:
            docIdHuntByWord(word)
    else:
        docIdHuntByWord(cleanQuery)

def signal_handler(_signal, frame):
    print("Goodbye!")
    sys.exit(0)

if __name__ == "__main__":
    ftrie = open("{}/trie.json".format(REUTERS_DIR), "r")
    finv_dict = open("{}/inv_dict.json".format(REUTERS_DIR), "r")

    trie = json.load(ftrie)
    inv_dict = json.load(finv_dict)

    print("Welcome!")
    print("This program is based on single word\nquery and single word prefix search.")
    print("To exit, enter ###.")
    while True:
        query_handler(input("Enter your search query:\n"))
        signal.signal(signal.SIGINT, signal_handler)
