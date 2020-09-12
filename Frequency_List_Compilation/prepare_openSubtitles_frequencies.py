files = [['es-2011.txt', 'OpenSubtitlesEs2011_WF.tsv'],
         ['es-2012.txt', 'OpenSubtitlesEs2012_WF.tsv'],
         ['es-2016.txt', 'OpenSubtitlesEs2016_WF.tsv'],
         ['es-2018.txt', 'OpenSubtitlesEs2018_WF.tsv'],
         ['fr-2011.txt', 'OpenSubtitlesFr2011_WF.tsv'],
         ['fr-2012.txt', 'OpenSubtitlesFr2012_WF.tsv'],
         ['fr-2016.txt', 'OpenSubtitlesFr2016_WF.tsv'],
         ['fr-2018.txt', 'OpenSubtitlesFr2018_WF.tsv']]

def process():
    for file in files:
        with open(f'OpenSubtitles_Frequency_Lists\\{file[0]}', 'r', encoding='utf-8') as f:
            content = f.read().replace(' ', '\t')

        with open(file[1], 'w', encoding='utf-8') as out:
            out.write(content)