import os
import re
import copy
import string
from constants import *

def stretch(matrix):
    '''
    Compresses the 2D Matrix into 1D array
    '''
    stretched = []
    for ix in matrix:
        for ixx in ix:
            stretched.append(ixx)
    return stretched

def fileInspector():
    '''
    Retrieves the name of files in reuters21578 directory
    e.g. if path of the reuters21578 directory is:
    - ~/Desktop/reuters21578/, then it checks ~/Desktop
    '''
    flist = sorted([ f for f in os.listdir("{}/reuters21578".format(REUTERS_DIR)) if "reut2" in f ], key=str.lower)
    return flist

def fileRead(location, fname):
    '''
    Retrieves the content of the given file name in reuters21578 directory
    '''
    with open("{}/reuters21578/{}".format(location, fname), "r", encoding=ENCODING) as f:
        return f.read()

def fileParse(content):
    '''
    Retrieves the matching reuters article
    '''
    return [match.group() for match in re.finditer(ARTICLE_REGEX, content)]

def titleParse(content):
    '''
    Retrieves the matching title data in a reuters article
    '''
    return [match.group(1) for match in re.finditer(TITLE_REGEX, content)]

def bodyParse(content):
    '''
    Retrieves the matching body data in a reuters article
    '''
    return [match.group(1) for match in re.finditer(BODY_REGEX, content)]

def removeTag(content, tags):
    '''
    Removes the xml tags of the data
    '''
    return list(map(lambda x: x.replace(tags[0], "").replace(tags[1], ""), content))

def getNewId(content):
    '''
    Retrieves the article id in a reuters article
    '''
    return [match.group(1) for match in re.finditer(NEWID_REGEX, content)]

def unfoldLines(content):
    '''
    Removes the newline indicators
    '''
    result = []
    lines = content.split("\n")
    for line in lines:
        result.append(line)
    return result

def trimLines(content):
    '''
    Removes any leading or trailing whitespaces.
    '''
    result = []
    for ess in content:
        result.append(str(ess).strip())
    return result

def clearPunc(content):
    '''
    Replaces any punctuation with a one space character
    '''
    result = []
    for ess in content:
        result.append(str(ess).translate(str.maketrans(string.punctuation, " "*len(string.punctuation))))
    return result

def caseFold(content):
    '''
    Converts any content into a lowercase version of itself
    '''
    result = []
    for ess in content:
        result.append(str(ess).lower())
    return result

def stopwords(content):
    '''
    Analyzes stopwords and removes the occuring stopwords from the content
    '''
    f = open("{}/stopwords.txt".format(REUTERS_DIR), "r")
    stops = f.readlines()
    strippedStops = [stop.strip("\n") for stop in stops]
    strippedStops = [stop.strip(" ") for stop in strippedStops]

    result = []
    isStart = True
    for stop in strippedStops:
        if isStart:
            processedTokens = content
            isStart = False
        else:
            processedTokens = copy.deepcopy(result)
            result = []
        for token in processedTokens:
            if str(stop) != str(token):
                result.append(token)

    f.close()
    return result

def tokenization(content):
    '''
    Tokenizes the given content, creates one-string tokens
    '''
    result = []
    for ess in content:
        tokens = ess.split()
        cleans = [token.strip() for token in tokens]
        for clean in cleans:
            result.append(clean)
    return result
