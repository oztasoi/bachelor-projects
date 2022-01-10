import copy as cp
import json as js
import random as rn

raw_model = None
feature_selection_model = None

def load_model_classifications():
    '''
    -> Loads the outputs of raw model classifications and
    feature selected model classifications to be used in
    randomizations
    '''
    global raw_model, feature_selection_model
    fin_raw = open("./output/raw_output.json", "r")
    raw_model = js.load(fin_raw)
    fin_raw.close()
    fin_feature_selection = open("./output/feature_selection_output.json", "r")
    feature_selection_model = js.load(fin_feature_selection)
    fin_feature_selection.close()

def calculate_f_measure(classifications):
    '''
    -> Returns the macro averages f-measure
    to be used in randomization test, regarding
    the given classification state
    '''
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

    precision_spam = correct_spam / 240
    precision_legitimate = correct_legitimate / 240

    recall_spam = correct_spam / (correct_spam + len(incorrect_legitimate_list))
    recall_legitimate = correct_legitimate / (correct_legitimate + len(incorrect_spam_list))

    macro_avg_precision = (precision_spam + precision_legitimate) / 2
    macro_avg_recall = (recall_spam + recall_legitimate) / 2
    macro_avg_f_measure = (2 * macro_avg_precision * macro_avg_recall) / (macro_avg_precision + macro_avg_recall)

    return macro_avg_f_measure

def randomization_test(abs_diff, iteration_count = 1000):
    '''
    -> Iterates by the iteration count to test the
    null hypothesis and returns the p-value
    '''
    global raw_model, feature_selection_model
    count = 0
    for _ in range(iteration_count):
        cp_raw_model = cp.deepcopy(raw_model)
        cp_feature_selection_model = cp.deepcopy(feature_selection_model)
        for docId in cp_raw_model.keys():
            calc_raw = cp_raw_model[docId]["calc"]
            calc_feature = cp_feature_selection_model[docId]["calc"]

            val = rn.random()
            # Swaps the values
            if val > 0.5:
                cp_feature_selection_model[docId]["calc"] = calc_raw
                cp_raw_model[docId]["calc"] = calc_feature

        macro_avg_f_raw = calculate_f_measure(cp_raw_model)
        macro_avg_f_feature = calculate_f_measure(cp_feature_selection_model)
        _abs_diff = abs(macro_avg_f_raw - macro_avg_f_feature)

        del cp_raw_model
        del cp_feature_selection_model

        # Checks whether the pseudo-state has more difference than the initial state
        if _abs_diff >= abs_diff:
            count += 1

    return (count + 1) / (iteration_count + 1)

if __name__ == "__main__":
    load_model_classifications()
    ic = 2000
    macro_f_measure_raw = calculate_f_measure(raw_model)
    macro_f_measure_feature = calculate_f_measure(feature_selection_model)
    abs_diff = abs(macro_f_measure_raw - macro_f_measure_feature) # Calculates the absolute difference in macro avg f-measures
    p_value = randomization_test(abs_diff, iteration_count=ic)
    print(f"p-value: {p_value} for R = {ic}")
