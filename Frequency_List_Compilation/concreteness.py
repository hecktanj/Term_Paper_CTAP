import numpy as np
import pandas as pd

from column_extractor import extract_columns


def process():
    # lemmas French
    # scale: 1-5
    with open(r'Frequency_Lists\1.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][2:])
    french_lemmas = extract_columns(content, 2, None, None)
    output_name = 'lemma_ConcretenessFR.tsv'
    output1 = [output_name, french_lemmas]

    # lemmas French aggregated:
    # scales: 1-5
    with open(r'Frequency_Lists\5.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c1 = extract_columns(content, 2, 1, 5)
    french_lemmas_aggregated = extract_columns(french_lemmas, 1, 1, 5)
    for el in c1:
        if not el in french_lemmas_aggregated[:, 0:1]:
            french_lemmas_aggregated = np.append(french_lemmas_aggregated, [el], axis=0)
    output_name = 'lemma_ConcretenessFR_aggregated.tsv'
    output2 = [output_name, french_lemmas_aggregated]

    # lemmas Spanish
    # scale: 1-7
    with open(r'Frequency_Lists\16.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])[:, 1:]
    spanish_lemmas = extract_columns(content, 9, None, None)
    output_name = 'lemma_ConcretenessES.tsv'
    output3 = [output_name, spanish_lemmas]

    return [output1, output2, output3]