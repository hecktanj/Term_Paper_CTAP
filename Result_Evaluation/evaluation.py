from math import sqrt

dict = {}
isFirst = True
with open('Results_2_texts.csv', 'rt', encoding="utf8") as f, open('Results_2_texts.csv', 'rt', encoding="utf8") as f2:
    for line, line2 in zip(f, f2):
        if isFirst:
            isFirst = False
        else:
            l = line.strip()
            l2 = line2.strip()
            if not l == '' and not l2 == '':
                cols = l.split('\t')
                cols2 = l2.split('\t')
                if not len(cols) == 6 or not len(cols2) == 6:
                    print(cols, cols2)
                else:
                    if cols[4] in dict:
                        dict[cols[4]].append(float(cols[5]) - float(cols2[5]))
                    else:
                        dict[cols[4]] = [float(cols[5]) - float(cols2[5])]

means = {k: sum(v)/len(v) for k, v in dict.items()}
sds = {k: sqrt(sum([(i - means[k]) ** 2 for i in v]) / (len(v) - 1)) for k, v in dict.items()}
zs = {k: [((i - means[k]) / sds[k] if not sds[k] == 0 else 0) for i in v] for k, v in dict.items()}
zmeans = {k: sum(v)/len(v) for k, v in zs.items()}
zsds = {k: sqrt(sum([(i - zmeans[k]) ** 2 for i in v]) / (len(v) - 1)) for k, v in zs.items()}

def print_dict(dict):
    for k in dict:
        print(f'{k}: {dict[k]}')

print_dict(means)
print_dict(sds)
print_dict(zs)
print_dict(zmeans)
print_dict(zsds)