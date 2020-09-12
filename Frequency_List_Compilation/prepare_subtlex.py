import math

import pandas as pd
import numpy as np

def process():
    content = pd.read_excel ('SUBTLEX-ESP.xlsx').to_numpy()
    content = np.concatenate((content[:, 0:4], content[:, 5:9], content[:, 10:14]), axis=0)

    with open('SUBTLEXesp_SUBTLWF.tsv', 'w') as out1:
        with open('SUBTLEXesp_SUBTLWFInMillion.tsv', 'w') as out2:
            with open('SUBTLEXesp_Log10WF.tsv', 'w') as out3:
                for i in range(len(content)):
                    if not str(content[i, 0]) == 'nan':
                        out1.write(str(content[i, 0]) + '\t' + str(content[i, 1]) + '\n')
                        out2.write(str(content[i, 0]) + '\t' + str(content[i, 2]) + '\n')
                        out3.write(str(content[i, 0]) + '\t' + str(content[i, 3]) + '\n')
