import numpy as np

from column_extractor import extract_columns


def process():
    # forms French
    # scale: 1-7
    with open(r'Frequency_lists\8.csv', "r", encoding='utf-8') as f:
       content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    french_forms = extract_columns(content, 3, None, None)
    output_name = 'ImageabilityFR.tsv'
    output1 = [output_name, french_forms]

    # lemmas French
    # scale: 1-7
    with open(r'Frequency_lists\10.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    french_lemmas = extract_columns(content, 4, None, None)
    output_name = 'lemma_ImageabilityFR.tsv'
    output2 = [output_name, french_lemmas]

    # lemmas French aggregated
    # scales: 1-5, 1-7, 1-7
    with open(r'Frequency_Lists\5.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c1 = extract_columns(content, 4, 1, 5)
    with open(r'Frequency_Lists\7.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c2 = extract_columns(content, 36, 1, 7)
    with open(r'Frequency_Lists\11.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c3 = extract_columns(content, 7, 1, 7)
    french_lemmas_aggregated = extract_columns(french_lemmas, 1, 1, 7)
    for el in np.concatenate((c1, c2, c3), axis=0):
        if not el in french_lemmas_aggregated[:, 0:1]:
            french_lemmas_aggregated = np.append(french_lemmas_aggregated, [el], axis=0)
    output3 = [output_name, french_lemmas_aggregated]


    # lemmas Spanish
    # scale: 1-8
    with open(r'Frequency_lists\15a.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')[4:]])
        content = np.concatenate((np.column_stack((content[:, 0], content[:, 2])), np.column_stack((content[:, 10], content[:, 12]))), axis=0)
    with open(r'Frequency_lists\15b.csv', "r") as f:
        content2 = np.array([line.split(';') for line in f.read().strip().split('\n')[4:]])
        content2 = np.concatenate((np.column_stack((content2[:, 0], content2[:, 2])), np.column_stack((content2[:, 10], content2[:, 12])), np.column_stack((content2[:, 19], content2[:, 21]))), axis=0)
    content = np.concatenate((content, content2), axis=0)
    new_content = []
    for line in content:
        if not line[0].strip() == '':
            new_content.append([line[0].split(' ')[0], line[1]])
    spanish_lemmas = extract_columns(np.array(new_content), 1, None, None)
    output_name = 'lemma_ImageabilityES.tsv'
    output4 = [output_name, spanish_lemmas]


    # forms Spanish
    # scale: 1-7
    with open(r'Frequency_Lists\16.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])[:, 1:]
    spanish_forms = extract_columns(content, 12, None, None)
    output_name = 'ImageabilityES.tsv'
    output5 = [output_name, spanish_forms]


    return [output1, output2, output3, output4, output5]