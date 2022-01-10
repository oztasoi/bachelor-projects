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

word_informativeness = dict()
feature_vocabulary = list()

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

def select_features(feature_count=100):
    '''
    -> By using each word in the vocabulary,
    it calculates its informativeness ratio and
    sorts all words in descending order, thus
    returns the top 100 words.
    '''
    global vocabulary, spam_corpus, legitimate_corpus, word_informativeness
    for word in vocabulary.keys():
        informativeness = 0.0
        '''
        -> Creates contingency table
        '''
        docs_contain_word_in_spam = contain_count(spam_corpus, word)
        docs_contain_word_in_legitimate = contain_count(legitimate_corpus, word)
        docs_not_contain_word_in_spam = 240 - docs_contain_word_in_spam
        docs_not_contain_word_in_legitimate = 240 - docs_contain_word_in_legitimate

        if docs_contain_word_in_spam != 0:
            informativeness += (docs_contain_word_in_spam / 480) * m.log2((480 * docs_contain_word_in_spam) / ((docs_contain_word_in_spam + docs_contain_word_in_legitimate) * (240)))

        if docs_contain_word_in_legitimate != 0:
            informativeness += (docs_contain_word_in_legitimate / 480) * m.log2((480 * docs_contain_word_in_legitimate) / ((docs_contain_word_in_legitimate + docs_contain_word_in_spam) * (240)))

        if docs_not_contain_word_in_spam != 0:
            informativeness += (docs_not_contain_word_in_spam / 480) * m.log2((480 * docs_not_contain_word_in_spam) / ((docs_not_contain_word_in_spam + docs_not_contain_word_in_legitimate) * (240)))

        if docs_not_contain_word_in_legitimate != 0:
            informativeness += (docs_not_contain_word_in_legitimate / 480) * m.log2((480 * docs_not_contain_word_in_legitimate) / ((docs_not_contain_word_in_legitimate + docs_not_contain_word_in_spam) * (240)))

        word_informativeness[word] = informativeness

    # Sorts the informativeness ratios
    word_informativeness = dict(sorted(word_informativeness.items(), key=lambda item: item[1], reverse=True))
    return list(word_informativeness.keys())[:feature_count]

def contain_count(_dict, _word):
    '''
    -> Calculates whether how many documents
    contain _word
    '''
    container = 0
    for corp in _dict.values():
        if _word in list(corp.keys()):
            container += 1
    return container

def calculate_nb_with_features(content, class_prob, isSpam=False):
    '''
    -> Uses the calculated top 100 features and
    calculates the Naive Bayesian values according to that.
    '''
    global spam_probs, legitimate_probs, feature_vocabulary
    if isSpam:
        probs = spam_probs
    else:
        probs = legitimate_probs

    fvoc = feature_vocabulary
    prob = float()
    prob += m.log2(class_prob)
    for word, freq in content.items():
        if word in fvoc:
            try:
                prob += m.log2(probs[word]) * freq
            except:
                pass
    return prob

def feature_model():
    global classifications
    spam_class_prob = 0.5
    legitimate_class_prob = 0.5

    test_spam_files = u.fileInspector(".", isTrain=False, isSpam=True)
    test_legitimate_files = u.fileInspector(".", isTrain=False, isSpam=False)

    for test_spam_f  in test_spam_files:
        content = u.fileRead("./dataset/test/spam/", test_spam_f)
        content = u.re.sub("Subject:", " ", content)
        content = u.clearPunc(content)
        content = u.processed_string(content)
        current_doc = dd(int)

        for token in content:
            current_doc[token] += 1

        spam_prob = calculate_nb_with_features(current_doc, spam_class_prob, isSpam=True) # Calculates Naive Bayesian with the selected features
        legitimate_prob = calculate_nb_with_features(current_doc, legitimate_class_prob, isSpam=False) # Calculates Naive Bayesian with the selected features

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

        spam_prob = calculate_nb_with_features(current_doc, spam_class_prob, isSpam=True) # Calculates Naive Bayesian with the selected features
        legitimate_prob = calculate_nb_with_features(current_doc, legitimate_class_prob, isSpam=False) # Calculates Naive Bayesian with the selected features

        # Evaluates the document
        if spam_prob > legitimate_prob:
            classifications[test_legitimate_f] = { "given": 0, "calc": 1 }
        else:
            classifications[test_legitimate_f] = { "given": 0, "calc": 0 }

def dump_features():
    '''
    -> Dumps the informativeness ratio and
    first 100 words to be accessed easily.
    '''
    global word_informativeness
    fout = open("./output/features.json", "w")
    dump_obj = { "word_informativeness": word_informativeness, "words": feature_vocabulary }
    json.dump(dump_obj, fout)
    fout.flush()
    fout.close()

def dump_precision(dump_obj):
    '''
    -> Dumps the feature selected version
    outputs to be used in randomization stage
    '''
    fout = open("./output/feature_selection_output.json", "w")
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

    print(f"FEATURE SELECTED: For spam class, {correct_spam} out of {total_spam} classified correctly.")
    print(f"FEATURE SELECTED: For legitimate class, {correct_legitimate} out of {total_legitimate} classified correctly.")

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

    print("WITH FEATURE SELECTION:")
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
    feature_vocabulary = select_features()
    dump_features()
    feature_model()
    calculate_precision()
