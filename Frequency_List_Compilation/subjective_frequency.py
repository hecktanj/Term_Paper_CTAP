import numpy as np

from column_extractor import extract_columns


def process():
    # forms French
    # scale: 1-7
    with open(r'Frequency_lists\8.csv', "r", encoding='utf-8') as f:
       content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    french_forms = extract_columns(content, 1, None, None)
    output_name = 'SubjFreqFR.tsv'
    output1 = [output_name, french_forms]


    # lemmas French
    # scale: 1-7
    with open(r'Frequency_lists\10.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    french_lemmas = extract_columns(content, 1, None, None)
    output_name = 'lemma_SubjFreqFR.tsv'
    output2 = [output_name, french_lemmas]


    # lemmas French aggregated
    # scales: 1-7
    with open(r'Frequency_Lists\11.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c1 = extract_columns(content, 6, 1, 7)
    french_lemmas_aggregated = extract_columns(french_lemmas, 1, 1, 7)
    for el in c1:
        if not el in french_lemmas_aggregated[:, 0:1]:
            french_lemmas_aggregated = np.append(french_lemmas_aggregated, [el], axis=0)
    output_name = 'lemma_SubjFreqFR_aggregated.tsv'
    output3 = [output_name, french_lemmas_aggregated]


    return [output1, output2, output3]