import numpy as np

from column_extractor import extract_columns


def process():
    # forms French
    # scale: 1-6
    with open(r'Frequency_Lists\3.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    french_forms = extract_columns(content, 3, None, None)
    last_form = None
    unique_forms = []
    for i in range(len(french_forms)):
        if french_forms[i, 0] == last_form:
            unique_forms[-1][1] = float(unique_forms[-1][1]) + float(french_forms[i, 1])
        else:
            unique_forms.append([french_forms[i, 0], french_forms[i, 1]])
            last_form = french_forms[i, 0]
    output_name = 'FamiliarityFR.tsv'
    output1 = [output_name, unique_forms]


    # lemmas Spanish
    # scale: 1-9
    with open(r'Frequency_lists\12.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    spanish_lemmas = extract_columns(content, 8, None, None)
    output_name = 'lemma_FamiliarityES.tsv'
    output2 = [output_name, spanish_lemmas]


    # forms Spanish
    # scale: 1-7
    with open(r'Frequency_Lists\16.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])[:, 1:]
    spanish_forms = extract_columns(content, 18, None, None)
    output_name = 'FamiliarityES.tsv'
    output3 = [output_name, spanish_forms]


    # lemmas Spanish aggregated
    # scales: 1-5
    with open(r'Frequency_lists\12.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c1 = extract_columns(content, 6, 1, 5)
    spanish_lemmas_aggregated = extract_columns(spanish_lemmas, 1, 1, 9)
    for el in c1:
        if not el in spanish_lemmas_aggregated[:, 0:1]:
            spanish_lemmas_aggregated = np.append(spanish_lemmas_aggregated, [el], axis=0)
    output_name = 'lemma_FamiliarityES_aggregated.tsv'
    output4 = [output_name, spanish_lemmas_aggregated]


    return [output1, output2, output3, output4]