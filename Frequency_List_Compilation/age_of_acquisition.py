import numpy as np

from column_extractor import extract_columns


def process():
    # forms French
    # scale: age in years
    output_name = 'AgeOfAcquisitionFR.tsv'
    with open(r'Frequency_lists\8.csv', "r", encoding='utf-8') as f:
       content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    min = np.amin(content[:,2].astype(np.float))
    max = np.amax(content[:,2].astype(np.float))
    French_forms = extract_columns(content, 2, None, None)
    output1 = [output_name, French_forms]

    # lemmas Spanish main
    # scale: 1 - 11
    output_name = 'lemma_AgeOfAcquisitionES.tsv'
    with open(r'Frequency_lists\14.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    Spanish_lemmas_main = extract_columns(content, 1, None, None)
    output2 = [output_name, Spanish_lemmas_main]

    # lemmas Spanish aggregated (keep values of each list and only add new entries)
    #  scales 1 - 11; 1 - 7
    output_name = 'lemma_AgeOfAcquisitionES_aggregated.tsv'
    with open(r'Frequency_lists\12.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')][1:])
    c1 = extract_columns(content, 14, 1, 11)

    with open(r'Frequency_lists\15a.csv', "r") as f:
        content = np.array([line.split(';') for line in f.read().strip().split('\n')[4:]])
        content = np.concatenate((content[:, 0:2], content[:, 10:12]), axis=0)
    with open(r'Frequency_lists\15b.csv', "r") as f:
        content2 = np.array([line.split(';') for line in f.read().strip().split('\n')[4:]])
        content2 = np.concatenate((content2[:, 0:2], content2[:, 10:12], content2[:, 19:21]), axis=0)
    content = np.concatenate((content, content2), axis=0)
    new_content = []
    for line in content:
        if not line[0].strip() == '':
            new_content.append([line[0].split(' ')[0], line[1]])
    c2 = extract_columns(np.array(new_content), 1, 1, 7)
    Spanish_lemmas_aggregated = extract_columns(Spanish_lemmas_main, 1, 1, 11)
    for el in c1:
        if not el in Spanish_lemmas_aggregated[:, 0:1]:
            Spanish_lemmas_aggregated = np.append(Spanish_lemmas_aggregated, [el], axis = 0)
    for el in c2:
        if not el in Spanish_lemmas_aggregated[:, 0:1]:
            Spanish_lemmas_aggregated = np.append(Spanish_lemmas_aggregated, [el], axis = 0)
    output3 = [output_name, Spanish_lemmas_aggregated]

    return [output1, output2, output3]