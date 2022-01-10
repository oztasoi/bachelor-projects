import sys
import json
import utils as u

from collections import defaultdict as dd

DIRECTORY_PREFIX = "dataset"
ALPHA = 1.0 # Specified alpha value, given in the description

vocabulary = dd(int) # Global vocabulary

spam_unified = dd(int) # One spam document including every subdocument word and its accumulative term frequency
legitimate_unified = dd(int) # One legitimate document including every subdocument word and its accumulative term frequency

spam_corpus = dd(dd) # Spam corpus holding every spam mail in the training set
legitimate_corpus = dd(dd) # Legitimate corpus holding every spam mail in the training set

spam_probs = dd(float) # Probabilities of words in spam documents
legitimate_probs = dd(float) # Probabilities of words in legitimate documents

def preprocess(_parent_directory):
    '''
    -> Reads every spam and legitimate file
    and calculates its effect on vocabulary,
    unified spam or legitimate doc.
    '''
    global spam_corpus, spam_unified, legitimate_corpus, legitimate_unified
    spam_files = u.fileInspector(_parent_directory, isTrain=True, isSpam=True)

    for f in spam_files:
        content = u.fileRead(f"{_parent_directory}/{DIRECTORY_PREFIX}/training/spam", f)
        content = u.re.sub("Subject:", " ", content)
        content = u.clearPunc(content)
        content = u.processed_string(content)
        current_doc = dd(int)

        for token in content:
            current_doc[token] += 1
            spam_unified[token] += 1
            vocabulary[token] += 1

        spam_corpus[f] = current_doc

    legitimate_files = u.fileInspector(_parent_directory, isTrain=True, isSpam=False)

    for f in legitimate_files:
        content = u.fileRead(f"{_parent_directory}/{DIRECTORY_PREFIX}/training/legitimate", f)
        content = u.re.sub("Subject:", " ", content)
        content = u.clearPunc(content)
        content = u.processed_string(content)
        current_doc = dd(int)

        for token in content:
            current_doc[token] += 1
            legitimate_unified[token] += 1
            vocabulary[token] += 1

        legitimate_corpus[f] = current_doc

def calculate_probs():
    '''
    -> Calculates each word in vocabulary,
    belongs to either spam or legitimate class
    '''
    global spam_unified, legitimate_unified, spam_probs, legitimate_probs, vocabulary
    spam_total_words = sum(spam_unified.values())
    legitimate_total_words = sum(legitimate_unified.values())
    vocabulary_length = len(vocabulary)
    for word in vocabulary.keys():
        spam_probs[word] = (spam_unified[word] + ALPHA) / (spam_total_words + ALPHA * vocabulary_length)
        legitimate_probs[word] = (legitimate_unified[word] + ALPHA) / (legitimate_total_words + ALPHA * vocabulary_length)

def dump_calculations():
    '''
    -> Dumps the calculated preprocessing information
    to be used in further stages.
    '''
    global vocabulary, spam_unified, spam_corpus, spam_probs, legitimate_unified, legitimate_corpus, legitimate_probs
    fout = open("./output/calculations.json", "w")
    calculations = { 
        "vocabulary": vocabulary,
        "spam_unified": spam_unified,
        "spam_corpus": spam_corpus,
        "spam_probs": spam_probs,
        "legitimate_unified": legitimate_unified,
        "legitimate_corpus": legitimate_corpus,
        "legitimate_probs": legitimate_probs
        }
    json.dump(calculations, fout)
    fout.close()

if __name__ == "__main__":
    preprocess(sys.argv[1])
    calculate_probs()
    dump_calculations()
