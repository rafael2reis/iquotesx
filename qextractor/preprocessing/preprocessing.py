# module preprocessing.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
preprocessing module - Prepares the data to the task

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
import csv
from pkg_resources import resource_filename

from qextractor.preprocessing import bosquequotes
from qextractor.preprocessing import baseline
from qextractor.preprocessing import verbspeech
from qextractor.preprocessing import feature

from qextractor.wis import wisinput

INDEX_QB = 4

BOSQUE_FILE = resource_filename('qextractor', 'data/corpus-bosquequotes-train.txt')
BOSQUE_TEST_FILE = resource_filename('qextractor', 'data/corpus-bosquequotes-test.txt')

INPUT_FILE = resource_filename('qextractor', 'data/gen/qextractor_input.csv')
INPUT_TEST_FILE = resource_filename('qextractor', 'data/gen/qextractor_input_test.csv')

def createInput(fileName=None, createTest=False):
    """Creates a CSV file with the result of the preprocessing step.

    Args:
        fileName: The CSV file that will be created
        createTest: If the preprocessing will be applyed in the test set
    """
    corpus = bosquequotes.load(BOSQUE_FILE)
    test = bosquequotes.load(BOSQUE_TEST_FILE)
    converter = verbspeech.Converter()

    if not fileName:
        fileName = INPUT_FILE

    open(fileName, 'w').close()

    pos = feature.pos(corpus + test, posIndex = 1)
    columns = feature.columns(pos)

    if createTest:
        corpus = test

    i = 0
    for i in range(len(corpus)):
        s = corpus[i]
        # qs = baseline.quotationStart(s)
        # qe = baseline.quotationEnd(s, qs)
        qb = baseline.quoteBounds(s)

        converter.vsay(s, tokenIndex = 0, posIndex = 1)

        #for k in range(len(s)):
        #    print(k, s[k][0].ljust(30), s[k][1].ljust(10), s[k][7].ljust(5), qs[k], qe[k], qb[k])

        # Baseline: X
        #print("Create bc...")
        bc = baseline.boundedChunk(s)
        #print("Create vsn...")
        vsn = baseline.verbSpeechNeighb(s)
        #print("Create fluc...")
        fluc = baseline.firstLetterUpperCase(s)

        #print("Identifying quotes...")
        # quotes = wisinput.interval(qb)

        #print("Identifying coreferences...")
        # coref, labels = wisinput.coref(s, quotes, corefIndex=7)
        quotes, coref, labels = wisinput.candidates(s, depIndex=2)

        #print("Creating features...")
        feat = feature.create(s, quotes=quotes, coref=coref, posIndex=1, corefIndex=3, quoteBounds=qb, bc=bc, vsn=vsn, fluc=fluc)

        #print("Binarying features...")
        bfeat = feature.binary(columns, feat)

        # Answer: Y
        #print("Output: Creating y...")
        qbA = [ e[INDEX_QB] for e in s ]

        #print("Output: Identifying quotes...")
        quotesA = wisinput.interval(qbA)
        #print("Output: Quotes = ", len(quotesA))

        #print("Output: Identifying coreferences...")
        corefA, labelsA = wisinput.corefAnnotated(s, quotes=quotesA, depIndex = 2, corefIndex = 3, quoteIndex = 4)
        #print("Output: Coref = ", len(corefA))

        print("Output: Creating features...")
        featA = feature.create(s, quotes=quotesA, coref=corefA, posIndex=1, corefIndex=3, \
                quoteBounds=qbA, bc=bc, vsn=vsn, fluc=fluc, dummy=False)

        #print("Output: Binarying features...")
        bfeatA = feature.binary(columns, featA)
        #print("Output: bFeat = ", len(bfeatA))

        with open(fileName, 'a', newline='') as csvfile:
            swriter = csv.writer(csvfile, delimiter=';')

            for p in range(len(bfeat)):
                for q in range(len(bfeat[p])):
                    swriter.writerow([i, "x"] + list(quotes[p]) + [labels[p][q]] + bfeat[p][q])

            for p in range(len(bfeatA)):
                for q in range(len(bfeatA[p])):
                    swriter.writerow([i, "y"] + list(quotesA[p]) + [labelsA[p][q]] + bfeatA[p][q])

        #print("Done!")

if __name__ == '__main__':
    createInput(fileName=INPUT_FILE, createTest=False)
    createInput(fileName=INPUT_TEST_FILE, createTest=True)
