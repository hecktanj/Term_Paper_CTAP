import age_of_acquisition
import concreteness
import familiarity
import frequency
import imageability
import prepare_lexique
import prepare_openSubtitles_frequencies
import prepare_subtlex
import subjective_frequency

#prepare_lexique.process()
#prepare_subtlex.process()
#prepare_openSubtitles_frequencies.process()

outputs = age_of_acquisition.process() + frequency.process() + concreteness.process() + familiarity.process() + subjective_frequency.process() + imageability.process()
for output in outputs:
    with open(f'output\\{output[0]}', 'w') as out:
        out.write('\n'.join(['\t'.join([str(e) for e in line]) for line in output[1]]))
