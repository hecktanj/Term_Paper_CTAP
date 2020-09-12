import pandas as pd

def process():
    content = pd.read_csv('Lexique383.tsv', sep='\t')
    form = content['ortho']
    freq_films = content['freqfilms2']
    freq_books = content['freqlivres']

    unique_frequencies = []
    last_form = None
    with open('lexiqueFilms_WFInMillion.tsv', 'w') as out1:
        with open('lexiqueBooks_WFInMillion.tsv', 'w') as out2:
            for i in range(len(form)):
                if form[i] == last_form:
                    unique_frequencies = [unique_frequencies[0] + freq_films[i], unique_frequencies[1] + freq_books[i]]
                else:
                    if not last_form is None:
                        out1.write(str(last_form) + '\t' + str(unique_frequencies[0]) + '\n')
                        out2.write(str(last_form) + '\t' + str(unique_frequencies[1]) + '\n')
                    unique_frequencies = [freq_films[i], freq_books[i]]
                    last_form = form[i]
            out1.write(str(last_form) + '\t' + str(unique_frequencies[0]) + '\n')
            out2.write(str(last_form) + '\t' + str(unique_frequencies[1]) + '\n')