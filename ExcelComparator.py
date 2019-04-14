# https://towardsdatascience.com/seven-clean-steps-to-reshape-your-data-with-pandas-or-how-i-use-python-where-excel-fails-62061f86ef9c
# https://stackoverflow.com/questions/48452933/python-comparison-ignoring-nan
# https://matthewkudija.com/blog/2018/07/21/excel-diff/

import os
import re
import pandas as pd

hypPath = ("C:\\dirTest\\hyperionDIR\\")
cogPath = ("C:\\dirTest\\cognosDIR\\")
hypFiles = os.listdir(hypPath)
cogFiles = os.listdir(cogPath)

for filename in hypFiles:
    print(filename)
    new_name = re.sub("^.{0,5}\_", '', filename)
    os.rename(hypPath + filename, hypPath + new_name)

for hypFilename in hypFiles:
    for cogFilename in cogFiles:
        if cogFilename == hypFilename:
            hypDf = pd.ExcelFile(hypPath + hypFilename)
            cogDf = pd.ExcelFile(cogPath + cogFilename)
            hypDf = hypDf.parse(0)
            cogDf = cogDf.parse(0)

        if hypDf.size >= cogDf.size:
            diffFile = hypDf.copy()
            # cogDf = cogDf.align(hypDf, axis=None)
            cogDf, hypDf = cogDf.align(hypDf, axis=None)
        else:
            diffFile = cogDf.copy()
            diffFile.fillna(0)
            hypDf = hypDf.align(cogDf, axis=None)

        for row in range(diffFile.shape[0]):
            for col in range(diffFile.shape[1]):
                value_OLD = hypDf.iloc[row, col]
                value_NEW = cogDf.iloc[row, col]
                if value_OLD == value_NEW:
                    diffFile.iloc[row, col] = cogDf.iloc[row, col]
                else:
                    diffFile.iloc[row, col] = ('{}→{}').format(value_OLD, value_NEW)

print(diffFile)

diffFile.to_excel("C:\\dirTest\\outputDIR\\compare - " + hypFilename, "compare")
