import os
import re
import string

punc = str()

def fileInspector(parent_directory, isTrain=False, isSpam=False):
    '''
    Retrieves the name of files in the directory
    e.g. if path of the <parent_directory> directory is:
    - ~/Desktop/<parent_directory>, then it checks ~/Desktop
    '''
    if isTrain:
        if isSpam:
            flist = sorted([ f for f in os.listdir( f"{parent_directory}/dataset/training/spam" ) if "msg" in f], key=str.lower)
        else:
            flist = sorted([ f for f in os.listdir( f"{parent_directory}/dataset/training/legitimate" ) if "msg" in f], key=str.lower)
    else:
        if isSpam:
            flist = sorted([ f for f in os.listdir( f"{parent_directory}/dataset/test/spam" ) if "msg" in f], key=str.lower)
        else:
            flist = sorted([ f for f in os.listdir( f"{parent_directory}/dataset/test/legitimate" ) if "msg" in f], key=str.lower)

    return flist

def fileRead(location, fname):
    '''
    Retrieves the content of the given file name in the given directory
    '''
    with open("{}/{}".format(location, fname), "r", encoding="latin-1") as f:
        return f.read()

def setPunc(isReset=False):
    '''
    - Creates punctuations to be removed in the string
    clearing operations, except it holds dollar sign
    since dollar sign seems to be exist very much in
    spam messages.
    '''
    global punc
    if isReset:
        punc = string.punctuation
    else:
        punc = string.punctuation
        dollar_sign_pos = punc.index("$")
        punc = punc[0:dollar_sign_pos] + punc[(dollar_sign_pos+1):]

def clearPunc(_string):
    '''
    - Clears any punctuation if necessary.
    '''
    global punc
    setPunc()
    non_punc_string = str(_string).translate(str.maketrans(punc, " "*len(punc)))
    setPunc(isReset=True)
    return non_punc_string

def processed_string(_string):
    '''
    - Splits the given string with respect to whitespace
    and make them lowercase while stripping any remaining
    whitespaces.
    '''
    current_form = clearPunc(_string)
    tokens = str(current_form).split()
    trimmed_tokens = []
    for token in tokens:
        trimmed_tokens.append(str(token).strip().lower())
    return trimmed_tokens
