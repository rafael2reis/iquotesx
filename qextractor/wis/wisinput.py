# module wisinput.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
wisinput module - Functions to create the input for WIS problem,
    given the quotations' attributes.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
#import globoquotes

def interval(qb, index = 0):
    """Creates an array with the quotations' interval.

    Args:
        qs: Array having a column with the quotation bounds annotation.
            A 'q' represents that the i-th token belongs to a quotation.
        index (optional): The index of the column in qs array with the
            quotation bounds annotation.

    Returns:
        An 1D array with tuples (s, e), where each tuple represents
        a quotation, being s the start index and e the end index.
    """
    intervals = []
    if type(qb[0]) is list:
        qb = [ e[index] for e in qb ]

    length = len(qb)
    inQuote = False
    s, e = 0, 0
    quoteIndex = -1
    for i in range(length):
        #print(i, qb[i])
        if qb[i] != '-':
            if not inQuote:
                s = i
                inQuote = True
                quoteIndex = qb[i]

            if (inQuote and ((i + 1 >= length) 
                    or (qb[i + 1] != quoteIndex))):
                e = i
                inQuote = False
                intervals.append( (s, e) )
                s, e = 0, 0

    return intervals

def coref(s, quotes, corefIndex):
    """
        two after the quotation and six before it

        Args:
            quotes:
            s: sentence in GloboQuotes format
            corefIndex: index of the column of s with coref information
        Returns:
            An array with the indexes of the coreferences
    """
    coref = []
    corefLabels = []

    for q in quotes:
        qstart = q[0]
        qend = q[1]

        index = []
        labels = ["dummy"]

        i = qend + 1
        n = 0
        while i < len(s) and n < 2:
            if s[i][corefIndex] != "O":
                if s[i-1][corefIndex] != s[i][corefIndex]:
                    index.append(i)
                    n += 1
            i += 1

        i = qstart - 1
        n = 0
        while i >= 0 and n < 6:
            if s[i][corefIndex] != "O":
                if s[i+1][corefIndex] != s[i][corefIndex]:
                    index.append(i)
                    n += 1
            i -= 1

        index.sort()
        for x in index:
            labels.append(s[x][corefIndex])
        coref.append(index)
        corefLabels.append(labels)

    return coref, corefLabels

def candidates(s, depIndex=2):
    intervals = []
    coref = []
    corefLabels = []

    length = len(s)
    # The candidates will be intervals of quotes or authors
    candidates = scanCandidates(s, depIndex)

    # print("wisinput.py s = ", s)
    # print("candidates: ", candidates)

    # Generate the combination of each
    for cand in candidates:
        #print("cand: ", cand)
        for x in cand:
            intervals.append(x)
            autInterval = []
            autLabels = ["dummy"]

            for y in cand:
                if x != y:
                    if y[1] < x[0]:
                        autInterval.append(y[1])
                    elif y[0] > x[1]:
                        autInterval.append(y[0])
                    autLabels.append( s[ y[0] ][depIndex] )
            coref.append(autInterval)
            corefLabels.append(autLabels)

    # print("intervals: ", intervals)
    # print("coref: ", coref)
    # print("corefLabels: ", corefLabels)

    return intervals, coref, corefLabels

def scanCandidates(s, depIndex=2):
    candidates = []
    length = len(s)
    b, e = 0, 0
    lastLabel = '-'
    rootIndex = ''
    c = []

    for i in range(length):
        if s[i][depIndex] != '-':
            if s[i][depIndex][-1] != rootIndex and rootIndex != '':
                candidates.append(c)
                c = []
            rootIndex = s[i][depIndex][-1]

            if s[i][depIndex][:4] != 'Root':
                if s[i][depIndex] != lastLabel:
                    b = i
                if i + 1 >= length or s[i + 1][depIndex] != s[i][depIndex]:
                    e = i
                    c.append( (b, e) )
                    b, e = 0, 0

            lastLabel = s[i][depIndex]
        else:
            lastLabel = '-'

        if (i + 1 >= length):
            candidates.append(c)

    return candidates

def corefAnnotated(s, quotes, depIndex = 2, corefIndex = 3, quoteIndex = 4):
    """Searches for the correct coreferences of the quotes given.

    Args:
        quotes: 2D array, which line having the quotation start and end indexes
        s: sentence in the BosqueQuotes format
    Returns:
        An array with the indexes of the coreferences. As the coreference
        could have up to two indexes, the closest index from the quote is
        the selected.
    """

    index = []
    labels = []

    length = len(s)
    b = 0

    for q in quotes:
        qstart = q[0]
        qend = q[1]

        qIndex = s[qstart][quoteIndex]
        inCoref = False
        for i in range(length):
            if s[i][corefIndex] == qIndex:

                if not inCoref:
                    if ((i > qend)
                            or ((i + 1 >= length) 
                                or (s[i + 1][corefIndex] != qIndex))):
                        index.append( [i] )
                        labels.append( [s[i][depIndex]] )
                        break

                    inCoref = True
                if (inCoref and ((i + 1 >= length) 
                        or (s[i + 1][corefIndex] != qIndex))):
                    if i < qstart:
                        index.append( [i] )
                        labels.append( [s[i][depIndex]] )
                        break

    return index, labels