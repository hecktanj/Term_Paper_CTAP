import os
import random
import re

def getTexts(directory):
    texts = {}
    current_text = ""
    save = False
    title = ""
    for filename in os.listdir(directory):
        with open(f'{directory}\\{filename}', 'rt', encoding="utf8") as f:
            for line in f:
                l = line.strip()
                if l.startswith('<SPEAKER'):
                    current_text = current_text.strip()
                    if not current_text == "" and save:
                        texts[title] = current_text
                    current_text = ""
                    if 'LANGUAGE="EN"' in l:
                        save = True
                        match = re.search(r'ID="?\d+', l)
                        title = filename + match.group()
                    else:
                        save = False
                else:
                    if save and not l.startswith('<'):
                        current_text += l + '\n'
            current_text = current_text.strip()
            if not current_text == "" and save:
                texts[title] = current_text
            save = False
    return texts

def align_texts(texts_es, texts_fr):
    tuples = []
    for key in texts_es:
        if key in texts_fr:
            tuples.append((texts_fr[key], texts_es[key]))
    return tuples

def select_random(texts):
    print(len(texts))
    random.shuffle(texts)
    return texts[0:1000]

def write_to_file(texts):
    if not os.path.exists(f'texts\\es'):
        os.makedirs(f'texts\\es')
    if not os.path.exists(f'texts\\fr'):
        os.makedirs(f'texts\\fr')

    counter = 1
    for text in texts:
        with open(f'texts\\fr\\{counter}.txt', "a", encoding="utf8") as f:
            f.write(text[0].strip())
        with open(f'texts\\es\\{counter}.txt', "a", encoding="utf8") as f:
            f.write(text[1].strip())
        counter += 1

def extract_files():
     spanish = getTexts('C:\\Users\\Tanja\\Downloads\\europarl\\europarl\\txt\\es')
     french = getTexts('C:\\Users\\Tanja\\Downloads\\europarl\\europarl\\txt\\fr')

     tuples = align_texts(spanish, french)
     #selected = select_random(tuples)
     write_to_file(tuples)