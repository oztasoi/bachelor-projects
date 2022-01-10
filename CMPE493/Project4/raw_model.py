import json
import math as m
import utils as u
from collections import defaultdict as dd

classifications = dd(int) # Results of the raw model classifications

vocabulary = None # Global vocabulary, calculated in preprocessing
spam_unified = None # Global unified spam doc, calculated in preprocessing
spam_corpus = None # Global spam corpus, calculated in preprocessing
spam_probs = None # Global probabilities of spam words, calculated in preprocessing
legitimate_unified = None # Global unified legitimate doc, calculated in preprocessing
legitimate_corpus = None # Global legitimate corpus, calculated in preprocessing
legitimate_probs = None # Global probabilities of legitimate words, calculated in preprocessing

def load_calculations():
    '''
    -> Loads the calculations, made in the
    previous stage
    '''
    global vocabulary, spam_unified, spam_corpus, spam_probs, legitimate_unified, legitimate_corpus, legitimate_probs
    fin = open("./output/calculations.json", "r")
    calculations = json.load(fin)
    vocabulary = calculations["vocabulary"]
    spam_unified = calculations["spam_unified"]
    spam_corpus = calculations["spam_corpus"]
    spam_probs = calculations["spam_probs"]
    legitimate_unified = calculations["legitimate_unified"]
    legitimate_corpus = calculations["legitimate_corpus"]
    legitimate_probs = calculations["legitimate_probs"]

def raw_model():
    global classifications
    spam_class_prob = 0.5 # Since we have 240 spam and 240 legitimate docs, each of these is 240 / (240 + 240) = 0.5
    legitimate_class_prob = 0.5

    test_spam_files = u.fileInspector(".", isTrain=False, isSpam=True)
    test_legitimate_files = u.fileInspector(".", isTrain=False, isSpam=False)

    for test_spam_f  in test_spam_files:
        content = u.fileRead("./dataset/test/spam/", test_spam_f)
        content = u.re.sub("Subject:", " ", content)
        content = u.clearPunc(content)
        content = u.processed_string(content) # Tokenizes
        current_doc = dd(int)

        for token in content:
            current_doc[token] += 1

        spam_prob = calculate_nb(current_doc, spam_class_prob, isSpam=True) # Calculate Naive Bayesian with all words
        legitimate_prob = calculate_nb(current_doc, legitimate_class_prob, isSpam=False) # Calculate Naive Bayesian with all words

        # Evaluates the document
        if spam_prob > legitimate_prob:
            classifications[test_spam_f] = { "given": 1, "calc": 1 }
        else:
            classifications[test_spam_f] = { "given": 1, "calc": 0 }

    for test_legitimate_f  in test_legitimate_files:
        content = u.fileRead("./dataset/test/legitimate/", test_legitimate_f)
        content = u.re.sub("Subject:", " ", content)
        content = u.clearPunc(content)
        content = u.processed_string(content)
        current_doc = dd(int)

        for token in content:
            current_doc[token] += 1

        spam_prob = calculate_nb(current_doc, spam_class_prob, isSpam=True) # Calculate Naive Bayesian with all words
        legitimate_prob = calculate_nb(current_doc, legitimate_class_prob, isSpam=False) # Calculate Naive Bayesian with all words

        # Evaluates the document
        if spam_prob > legitimate_prob:
            classifications[test_legitimate_f] = { "given": 0, "calc": 1 }
        else:
            classifications[test_legitimate_f] = { "given": 0, "calc": 0 }

def calculate_nb(content, class_prob, isSpam=False):
    '''
    -> Calculates the Naive Bayesian value
    with the probabalities, calculated in
    the previous stage.
    -> Uses logarithmic version
    '''
    global spam_probs, legitimate_probs
    if isSpam:
        probs = spam_probs
    else:
        probs = legitimate_probs

    prob = float()
    prob += m.log2(class_prob)
    for word, freq in content.items():
        try:
            prob += m.log2(probs[word]) * freq
        except:
            pass
    return prob

def dump_precision(dump_obj):
    '''
    -> Dumps the current output to be used in
    further stages
    '''
    fout = open("./output/raw_output.json", "w")
    json.dump(dump_obj, fout)
    fout.flush()
    fout.close()

def calculate_precision():
    '''
    -> Calculates the required performance statistics
    precision, recall, f-measure and its macro versions
    '''
    global classifications
    total_spam = 0
    correct_spam = 0
    incorrect_spam_list = list()
    total_legitimate = 0
    correct_legitimate = 0
    incorrect_legitimate_list = list()
    for doc, eval in classifications.items():
        given = eval["given"]
        if given == 1:
            total_spam += 1
            calc = eval["calc"]
            if calc == 1:
                correct_spam += 1
            else:
                incorrect_spam_list.append(doc)
        else:
            total_legitimate += 1
            calc = eval["calc"]
            if calc == 1:
                incorrect_legitimate_list.append(doc)
            else:
                correct_legitimate += 1

    print(f"For spam class, {correct_spam} out of {total_spam} classified correctly.")
    print(f"For legitimate class, {correct_legitimate} out of {total_legitimate} classified correctly.")
    
    dump_precision(classifications)

    precision_spam = correct_spam / 240
    precision_legitimate = correct_legitimate / 240

    recall_spam = correct_spam / (correct_spam + len(incorrect_legitimate_list))
    recall_legitimate = correct_legitimate / (correct_legitimate + len(incorrect_spam_list))

    f_measure_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
    f_measure_legitimate = (2 * precision_legitimate * recall_legitimate) / (precision_legitimate + recall_legitimate)

    macro_avg_precision = (precision_spam + precision_legitimate) / 2
    macro_avg_recall = (recall_spam + recall_legitimate) / 2
    macro_avg_f_measure = (2 * macro_avg_precision * macro_avg_recall) / (macro_avg_precision + macro_avg_recall)

    print("WITHOUT FEATURE SELECTION:")
    print(f"\tPRECISION OF SPAM: {precision_spam}")
    print(f"\tPRECISION OF LEGITIMATE: {precision_legitimate}")
    print(f"\tRECALL OF SPAM: {recall_spam}")
    print(f"\tRECALL OF LEGITIMATE: {recall_legitimate}")
    print(f"\tF-MEASURE OF SPAM: {f_measure_spam}")
    print(f"\tF-MEASURE OF LEGITIMATE: {f_measure_legitimate}")
    print(f"\tMACRO-AVG PRECISION: {macro_avg_precision}")
    print(f"\tMACRO-AVG RECALL: {macro_avg_recall}")
    print(f"\tMACRO-AVG F-MEASURE: {macro_avg_f_measure}")

if __name__ == "__main__":
    load_calculations()
    raw_model()
    calculate_precision()
