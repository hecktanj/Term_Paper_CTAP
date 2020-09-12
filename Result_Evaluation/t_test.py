import math
import statistics

import numpy as np
from matplotlib.gridspec import GridSpec

from scipy import stats
import matplotlib.pyplot as plt
from sympy.stats.frv_types import scipy
import pingouin as pn


def extract_feature_results(filename):
    lines = {}
    isFirst = True
    with open(filename, 'rt', encoding="utf8") as f:
        for line in f:
            if isFirst:
                isFirst = False
            else:
                l = line.strip()
                if not l == '':
                    cols = l.split('\t')
                    if not len(cols) == 6:
                        print(cols)
                    else:
                        text = int(cols[2].strip()[:-4])
                        if not text in lines:
                            lines[text] = {}
                        if cols[4] in lines[text]:
                            lines[text][cols[4]].append(float(cols[5]))
                        else:
                            lines[text][cols[4]] = [float(cols[5])]

    list = [lines[key] for key in sorted(lines.keys())]
    dict = {}
    for d in list:
        if len(dict) == 0:
            dict = d
        else:
            for key in d:
                dict[key].append(d[key][0])

    if 'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (LW Type)' in dict:
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (LW Type)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (LW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (LW Token)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (LW Token)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (FW Type)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (FW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (FW Token)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (FW Token)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (AW Type)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (AW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (AW Token)'] = dict[
            'Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (AW Token)']

        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (LW Type)']
        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (LW Token)']
        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (FW Type)']
        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (FW Token)']
        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (AW Type)']
        del dict['Lexical Sophistication Feature: LEXIQUE films Word Frequency Per Million Words (AW Token)']
    else:
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (LW Type)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (LW Token)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Token)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (FW Type)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (FW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (FW Token)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (FW Token)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (AW Type)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Type)']
        dict['Lexical Sophistication Feature: Word Frequency per Million Words (AW Token)'] = dict[
            'Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Type)']

        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Type)']
        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (LW Token)']
        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (FW Type)']
        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (FW Token)']
        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (AW Type)']
        del dict['Lexical Sophistication Feature: SUBTLEX Word Frequency (AW Token)']

    del dict['Lexical Sophistication Feature: Imageability (LW Token)']
    del dict['Lexical Sophistication Feature: Imageability (FW Type)']
    del dict['Lexical Sophistication Feature: Imageability (FW Token)']
    del dict['Lexical Sophistication Feature: Imageability (AW Type)']
    del dict['Lexical Sophistication Feature: Imageability (AW Token)']
    del dict['Lexical Sophistication Feature: Imageability (LW Type)']


    return dict

def calculate_t_test(es, fr):
    feature_values = {}
    for feature in es:
        feature_values[feature] = stats.ttest_ind(es[feature], fr[feature], equal_var=False)

    return feature_values

def get_best_features(features):
    # remove all features with p-values higher than 0.05 or nan
    # keys_to_remove = []
    # for key in features:
    #     if features[key][1] > 0.05 or math.isnan(features[key][1]):
    #         keys_to_remove.append(key)
    # for key in keys_to_remove:
    #     del features[key]

    # sort according to t-value
    return sorted(features.items(), key=lambda x: abs(x[1][0]), reverse=True)

def t_test_per_category(es, fr):
    dict = {}
    categories = []
    with open('features_per_category.tsv', 'rt', encoding="utf8") as f:
        for line in f:
            l = line.strip()
            if not l == '':
                cols = l.split('\t')
                dict[cols[1]] = cols[0]
                categories.append(cols[0])

    for cat in set(categories):
        es_reduced = {}
        fr_reduced = {}
        for key in es:
            if dict[key] == cat:
                es_reduced[key] = es[key]
                fr_reduced[key] = fr[key]

        features = calculate_t_test(es_reduced, fr_reduced)

        features = sorted(features.items(), key=lambda x: abs(x[1][0]), reverse=True)

        print(f'\n{cat}:')
        for k in features:
            print(f'{k[0]}: t-value={k[1][0]}, p-value={k[1][1]}')

def rank_categories(features):
    dict = {}
    categories = []
    with open('features_per_category.tsv', 'rt', encoding="utf8") as f:
        for line in f:
            l = line.strip()
            if not l == '':
                cols = l.split('\t')
                dict[cols[1]] = cols[0]
                categories.append(cols[0])

    cats = {}
    counter = 0
    for el in features:
        counter += 1
        if not dict[el[0]] in cats:
            cats[dict[el[0]]] = 0
        cats[dict[el[0]]] += counter
        counter += 1

    for c in cats:
        cats[c] /= counter
        print(f'{c}: {cats[c]}')

def get_absolute_values(es, fr):
    averages = {}
    for feature in es:
        averages[feature] = (sum(es[feature]) / len(es[feature]), sum(fr[feature]) / len(fr[feature]))
        print(f'{feature}: es: {averages[feature][0]}; fr: {averages[feature][1]}')
    return averages

def get_color(y):
    if y == 'Propositional Complextiy':
        return 'b'
    elif y == 'Lexical Complexity':
        return 'g'
    elif y == 'Syntactic Complexity':
        return 'm'
    elif y == 'General Text Length':
        return 'c'
    elif y == 'Morpho-syntactic Complexity':
        return 'y'

def create_plot(features, cohen = None, mean_sd_es = None, mean_sd_fr = None):
    sorted_features = sorted(features.items(), key=lambda x: 0 if math.isnan(x[1][0]) else abs(x[1][0]), reverse=True)
    sorted_features = sorted(cohen.items(), key=lambda x: 0 if math.isnan(x[1]) else abs(x[1]), reverse=True)

    dict = {}
    with open('features_per_category.tsv', 'rt', encoding="utf8") as f:
        for line in f:
            l = line.strip()
            if not l == '':
                cols = l.split('\t')
                dict[cols[1]] = cols[0]

    l1 = []
    l2 = []
    l3 = []
    for key in features:
        if math.isnan(cohen[key]) or cohen[key] == 0:
            name = [idx for idx, element in enumerate(sorted_features) if element[0] == key][0]
            l3.append((name + 1, 0, dict[key]))
        elif cohen[key] > 0:
            name = [idx for idx, element in enumerate(sorted_features) if element[0] == key][0]
            l1.append((name + 1, cohen[key], dict[key]))
        elif cohen[key] < 0:
            name = [idx for idx, element in enumerate(sorted_features) if element[0] == key][0]
            l2.append((name + 1, cohen[key], dict[key]))

    for key in sorted_features:
        if not cohen is None:
            print(f'{sorted_features.index(key) + 1} & {key[0]} & {dict[key[0]]} & {round(features[key[0]][0], 2)} & {round(features[key[0]][1], 3)} & {round(cohen[key[0]], 2)} & {round(mean_sd_fr[key[0]][0], 2)} & {round(mean_sd_fr[key[0]][1], 2)} & {round(mean_sd_es[key[0]][0], 2)} & {round(mean_sd_es[key[0]][1], 2)}\\\\')
        else:
            print(f'{sorted_features.index(key) + 1} & {key[0]} & {dict[key[0]]} & {round(features[key[0]][0], 2)} & {round(features[key[0]][1], 3)}\\\\')

    fig = plt.figure()
    plt.yticks([1, 2, 3])
    fig.show()
    ax = fig.add_subplot(111)

    for y in l1:
        ax.plot(y[1], 1, c=get_color(y[2]), marker="o")
        #plt.annotate(y[0], (1, y[1]))
    for y in l2:
        ax.plot(abs(y[1]), 2, c=get_color(y[2]), marker="^")
        #plt.annotate(y[0], (2, abs(y[1])))
    for y in l3:
        ax.plot(y[1], 3, c=get_color(y[2]), marker="s")
        #plt.annotate(y[0], (3, y[1]))

    plt.draw()
    plt.savefig('plt1.png')

    fig = plt.figure()
    plt.yticks([1, 2, 3])
    fig.show()
    ax = fig.add_subplot(111)

    for y in l1:
        if not (y[0] in [1, 2, 3, 4, 6, 9]):
            ax.plot(y[1], 1, c=get_color(y[2]), marker="o")
            #plt.annotate(y[0], (1, y[1]))
    for y in l2:
        ax.plot(abs(y[1]), 2, c=get_color(y[2]), marker="^")
        #plt.annotate(y[0], (2, abs(y[1])))
    for y in l3:
        ax.plot(y[1], 3, c=get_color(y[2]), marker="s")
        #plt.annotate(y[0], (3, y[1]))

    ax.axvline(x=90, c='r')
    plt.draw()
    plt.savefig('plt2.png')


def perform_t_test():
    es = extract_feature_results('Results_es.csv')
    fr = extract_feature_results('Results_fr.csv')
    features = calculate_t_test(es, fr)
    create_plot(features)
    #statistically_significant_features = get_best_features(features)

    #for k in statistically_significant_features:
    #    print(f'{k[0]}: t-value={k[1][0]}, p-value={k[1][1]}')
    #print('')
    #for k in es:
    #    print(k)

    #t_test_per_category(es, fr)
    #rank_categories(statistically_significant_features)
    #get_absolute_values(es, fr)

def check_t_test_applicability():
    es = extract_feature_results('Results_es.csv')
    fr = extract_feature_results('Results_fr.csv')

    sample_groups_es = create_sample_groups(es)
    sample_groups_fr = create_sample_groups(fr)

    shapiro_es = calculate_shapiro(sample_groups_es)
    shapiro_fr = calculate_shapiro(sample_groups_fr)

    # p-value has to be >.05 in order to indicate normal distribution
    all_normal = True
    for feature in shapiro_es:
        if shapiro_es[feature][1] < 0.05 or shapiro_fr[feature][1] < 0.05:
            all_normal = False
        else:
            f, p = perform_f_test(es, fr, feature)
            if p > 0.05:
                print(f'{feature}: normally distributed and similar variances')

    print(f'All normally distributed: {all_normal}')
    return all_normal


def calculate_shapiro(sample_groups):
    feature_values = {}
    for sample_group in sample_groups:
        for feature in sample_group:
            w_fr, p_fr = stats.shapiro(sample_group[feature])
            if not feature in feature_values:
                feature_values[feature] = []
            feature_values[feature].append((w_fr, p_fr))

    averages = {}
    for feature in feature_values:
        w_avg = np.mean([x[0] for x in feature_values[feature]])
        p_avg = np.mean([x[1] for x in feature_values[feature]])
        averages[feature] = (w_avg, p_avg)

    return averages

def create_sample_groups(samples):
    '''
    Shapiro-Wilk test is only reliable with max. 5000 samples.
    I we use subsamples and average, we can still use the p-value.
    --> http://www.real-statistics.com/tests-normality-and-symmetry/statistical-tests-normality-symmetry/shapiro-wilk-expanded-test/
    '''
    k = next(iter(samples.items()))[0]
    sample_count = len(samples[k])
    sample_groups = int(math.ceil(sample_count / 5000)) if sample_count > 5000 else 1
    groups = []
    for n in range(sample_groups):
        groups.append({})
    counter = 0
    group_index = 0
    while counter < sample_count:
        for feature in samples:
            if not feature in groups[group_index]:
                groups[group_index][feature] = []
            groups[group_index][feature].append(samples[feature][counter])
        group_index = (group_index + 1) % sample_groups
        counter += 1

    return groups


def perform_f_test(samples_es, samples_fr, feature):
    x = np.array(samples_es[feature])
    y = np.array(samples_fr[feature])
    f = np.var(x, ddof=1) / np.var(y, ddof=1)
    dfn = x.size - 1
    dfd = y.size - 1
    p = 1 - scipy.stats.f.cdf(f, dfn, dfd)
    return f, p


def calcualte_wilcoxon():
    es = extract_feature_results('Results_es.csv')
    fr = extract_feature_results('Results_fr.csv')

    features = calculate_wilcoxon_signed_rank(es, fr)
    # features = calculate_wilcoxon_sum_rank(es, fr)
    features_cohen = calculate_cohens_d(es, fr)
    mean_sd_fr = calculate_mean_sd(fr)
    mean_sd_es = calculate_mean_sd(es)

    create_plot(features, features_cohen, mean_sd_es, mean_sd_fr)



def calculate_wilcoxon_signed_rank(es, fr):
    feature_values = {}
    for feature in es:
        feature_values[feature] = stats.wilcoxon(es[feature], fr[feature], zero_method='zsplit')

    return feature_values

def calculate_wilcoxon_sum_rank(es, fr):
    feature_values = {}
    for feature in es:
        feature_values[feature] = stats.ranksums(es[feature], fr[feature])

    return feature_values

def calculate_cohens_d(es, fr):
    feature_values = {}
    for feature in es:
        feature_values[feature] = pn.compute_effsize(fr[feature], es[feature], eftype='cohen')

    return feature_values

def calculate_mean_sd(samples):
    feature_values = {}
    for feature in samples:
        mean = statistics.mean(samples[feature])
        sd = statistics.stdev(samples[feature])
        feature_values[feature] = (mean, sd)

    return feature_values


def get_statistics_box_plots():
    es = extract_feature_results('Results_es.csv')
    fr = extract_feature_results('Results_fr.csv')

    # create_overall_plot(es, fr)
    create_per_category_plots(es, fr)


def create_per_category_plots(es, fr):
    categories = {}
    with open('features_per_category.tsv', 'rt', encoding="utf8") as f:
        for line in f:
            l = line.strip()
            if not l == '':
                cols = l.split('\t')
                if not cols[0] in categories:
                    categories[cols[0]] = []
                categories[cols[0]].append(cols[1])

    fig = plt.figure()
    plt.axis("off")


    statistics = get_statistics(es, fr)
    ax = fig.add_subplot(231)
    ax.set_title('All measures', fontsize=9)
    flierprops = dict(markerfacecolor=(0.2, 0, 0.6, 0.2), markeredgecolor=(0.2, 0, 0.6, 0.2),
                      linestyle='none')
    bp = ax.boxplot(statistics.values(), flierprops=flierprops)
    ax.set_xticklabels(statistics.keys())
    plt.xlabel('Language with higher values', fontsize=8)
    plt.ylabel('Number of features', fontsize=8)
    plt.setp(bp['fliers'], markersize=2.0)


    counter = 2
    for cat in categories:
        statistics = get_statistics(es, fr, categories, cat)

        ax = fig.add_subplot(230 + counter)
        counter += 1

        add_subplot(ax, cat, statistics)

    plt.tight_layout()

    plt.draw()
    plt.savefig('per_category_statistics.png')


def add_subplot(ax, cat, statistics):
    ax.set_title(cat, fontsize=9)
    flierprops = dict(markerfacecolor=(0.2, 0, 0.6, 0.2), markeredgecolor=(0.2, 0, 0.6, 0.2),
                      linestyle='none')
    bp = ax.boxplot(statistics.values(), flierprops=flierprops)

    ax.set_xticklabels(statistics.keys())

    plt.xlabel('Language with higher values', fontsize=8)
    plt.ylabel('Number of features', fontsize=8)
    plt.setp(bp['fliers'], markersize=2.0)

def create_overall_plot(es, fr):
    statistics = get_statistics(es, fr)

    fig = plt.figure()
    plt.xlabel('Language with higher values')
    plt.ylabel('Number of features')

    fig.show()
    ax = fig.add_subplot(111)
    ax.set_title('All measures', fontsize=9)
    flierprops = dict(markerfacecolor=(0.2, 0, 0.6, 0.2), markeredgecolor=(0.2, 0, 0.6, 0.2),
                      linestyle='none')
    bp = ax.boxplot(statistics.values(), flierprops)
    plt.setp(bp['fliers'], markersize=2.0)
    plt.xlabel('Language with higher values', fontsize=8)
    plt.ylabel('Number of features', fontsize=8)
    ax.set_xticklabels(statistics.keys())

    plt.draw()
    plt.savefig('overall_statistics.png')

def get_statistics(es, fr, categories = None, cat = None):
    statistics_es = []
    statistics_fr = []
    statistics_same = []

    sample_count = len(es[next(iter(es.items()))[0]])
    counter = 0
    while counter < sample_count:
        count_es_larger = 0
        count_fr_larger = 0
        count_same = 0
        for feature in es:
            if cat is None or feature in categories[cat]:
                if es[feature][counter] > fr[feature][counter]:
                    count_es_larger += 1
                elif fr[feature][counter] > es[feature][counter]:
                    count_fr_larger += 1
                else:
                    count_same += 1

        statistics_es.append(count_es_larger)
        statistics_fr.append(count_fr_larger)
        statistics_same.append(count_same)
        counter += 1

    return {'ES': statistics_es, 'FR': statistics_fr, 'ND': statistics_same}