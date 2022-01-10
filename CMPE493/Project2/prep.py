import json

from utils import *
from constants import REUTERS_DIR

inv_dict = {}
trie = {}

def indexification(content, new_id):
    '''
    Creates a dictionary where first layer keys
    are all of the occuring words in whole articles
    and second layer keys are all of the occuring 
    article ids of that word, and its value is the
    frequency of that word in that article.
    - ess is my own abbreviation of essence as word.
    '''
    for ess in content:
        if ess not in inv_dict.keys():
            inv_dict[ess] = { new_id: 1 }
        else:
            if new_id not in inv_dict[ess].keys():
                currentState = inv_dict[ess]
                currentState[new_id] = 1
                inv_dict[ess] = currentState
            else:
                inv_dict[ess][new_id] += 1

def triefication(content):
    '''
    Creates a dictionary of recursive dictionaries
    where each key is a char and its value is either
    an empty dict when that key character is the last
    character of a word or a dict which contains chars
    as keys and their values as key-value pairs.
    - ess is my own abbreviation of essence as word.
    '''
    for ess in content:
        current_pos = trie
        for char in ess:
            if char not in current_pos.keys():
                current_pos[char] = {}
            current_pos = current_pos[char]

def dumpTrie():
    fout = open("{}/trie.json".format(REUTERS_DIR), "w")
    fout.write(json.dumps(trie))
    fout.flush()
    fout.close()

def dumptInvIndex():
    fout = open("{}/inv_dict.json".format(REUTERS_DIR), "w")
    fout.write(json.dumps(inv_dict))
    fout.flush()
    fout.close()

def extractData():
    fnames = fileInspector() # retrieves file names
    fcontents = [fileRead(REUTERS_DIR, name) for name in fnames] # retrieves file contents
    articles = stretch([fileParse(content) for content in fcontents]) # retrieves parsed articles in all files
    article_count = len(articles) # number of articles
    one_twentieth = int(article_count / 20) # related with the loading bar.
    loading_bar_count = 0 # related with the loading bar.

    for ix, article in enumerate(articles):
        if ix % one_twentieth == 0:
            print("{}/{} has been processed. | {}{} :)".format(ix, article_count, "#"*loading_bar_count, "."*(20-loading_bar_count)), end="\r")
            loading_bar_count += 1
        new_id_data = getNewId(article) # retrieve article id
        title_data = titleParse(str(article)) # retrieve title in the article
        body_data = bodyParse(str(article)) # retrieve body int the article

        pureTitle = [] # extracted title data
        if len(title_data) > 0:
            pureTitle = unfoldLines(title_data[0]) # remove newline characters if exist
            pureTitle = trimLines(pureTitle) # remove whitespaces if exist

        pureBody = [] # extracted body data
        if len(body_data) > 0:
            pureBody = unfoldLines(body_data[0]) # remove newline characters if exist
            pureBody = trimLines(pureBody) # remove whitespaces if exist

        pureData = pureTitle + pureBody # collect title and body data into one list
        if len(pureData) == 0: # if empty, that article does not work for the project
            continue

        pureData = tokenization(pureData) # initial tokenization of data
        caseFolded = caseFold(pureData) # lowercase all data
        noStopWords = stopwords(caseFolded) # remove stopwords from data
        noPunctuation = clearPunc(noStopWords) # remove punctuation of any kind
        finalTokens = tokenization(noPunctuation) # remove whitespaces and tokenize previously punctuated tokens

        indexification(finalTokens, new_id_data[0]) # create inverted indexes
        triefication(finalTokens)

    print("{}/{} has been processed. | {}{} :)".format(article_count, article_count, "#"*loading_bar_count, "."*(20-loading_bar_count)))

    dumpTrie() # dumps trie structure into a file
    dumptInvIndex() # dumps inverted index structure into a file

extractData()
