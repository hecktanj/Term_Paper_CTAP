import math

import numpy as np
import pandas as pd


def process():
    # forms and lemma French
    with open(r'Frequency_Lists\Lexique383.tsv', "r", encoding='utf-8') as f:
        content = np.array([line.split('\t') for line in f.read().strip().split('\n')][1:])
    last_form = None
    French_forms_films = []
    French_forms_books = []
    French_lemmas_films = []
    French_lemmas_books = []
    for i in range(len(content)):
        if content[i, 0] == last_form:
            French_forms_films[-1][1] = float(French_forms_films[-1][1]) + float(content[i, 8])
            French_forms_books[-1][1] = float(French_forms_books[-1][1]) + float(content[i, 9])
        else:
            French_forms_films.append([content[i, 0], content[i, 8]])
            French_forms_books.append([content[i, 0], content[i, 9]])
            last_form = content[i, 0]
        if int(content[i,13]) == 1:
            French_lemmas_films.append([content[i, 2], content[i, 6]])
            French_lemmas_books.append([content[i, 2], content[i, 7]])
    output_name = 'lexiqueFilms_WFInMillion.tsv'
    output1 = [output_name, French_forms_films]
    output_name = 'lexiqueBooks_WFInMillion.tsv'
    output2 = [output_name, French_forms_books]
    output_name = 'lemma_lexiqueFilms_WFInMillion.tsv'
    output3 = [output_name, French_lemmas_films]
    output_name = 'lemma_lexiqueBooks_WFInMillion.tsv'
    output4 = [output_name, French_lemmas_books]


    # forms Spanish
    output_name1 = 'SUBTLEXesp_SUBTLWF.tsv'
    output_name2 = 'SUBTLEXesp_SUBTLWFInMillion.tsv'
    output_name3 = 'SUBTLEXesp_Log10WF.tsv'
    content = pd.read_excel(r'Frequency_Lists\SUBTLEX-ESP.xlsx').to_numpy()
    content = np.concatenate((content[:, 0:4], content[:, 5:9], content[:, 10:14]), axis=0)
    new_content = []
    for row in content:
        if not math.isnan(float(row[1])):
            new_content.append(row)
    content = np.array(new_content)
    spanish_forms = np.column_stack((content[:, 0], content[:, 1].astype(int)))
    output5 = [output_name1, spanish_forms]
    spanish_forms_inMio = np.column_stack((content[:, 0], content[:, 2]))
    output6 = [output_name2, spanish_forms_inMio]
    spanish_forms_log = np.column_stack((content[:, 0], content[:, 3]))
    output7 = [output_name3, spanish_forms_log]

    return [output1, output2, output3, output4, output5, output6, output7]