# module baseline.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
baseline module - Functions to produce the Baseline System's features.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
#import globoquotes

CORPUS_DEP_INDEX = 2 # Index of Dependency Column in Corpus
CORPUS_POS_INDEX = 1

def boundedChunk(s):
    """Indetifies the Bounded Chunk.

    Assigns a 1 to the tokens that are part of
    a possible quotation. 
    
    Otherwise, assigns a 0 to the token.

    Args:
        s: 2D array that represents a sentence in the BosqueQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a bounded chunk.
    """
    bc = [ 0 for i in range(len(s))]

    a = [ e[0] for e in s ]

    for i in range(len(s)):
        #print(m.start(0), m.end(0))
        #print(m.group(0))
        if s[i][CORPUS_DEP_INDEX] != '-' and s[i][CORPUS_DEP_INDEX][:4] != 'Root':
            bc[i] = 1

    return bc

def firstLetterUpperCase(s):
    """Indetifies the tokens with First Letter Upper Case.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a token that starts with upper letter case.
    """
    uc = [ 0 for e in s ]
    tokenIndex = 0
    pattern = re.compile(r"\w+")

    for i in range(len(s)):
        # print("# baseline.py: ", s[i])
        text = s[i][tokenIndex][0]
        if re.match(pattern, text) and text == text.upper():
            uc[i] = 1

    return uc

def verbSpeechNeighb(s):
    """Indetifies the Verb of Speech Neighbourhood.

    Assigns a 1 to each verb of speech and also to its four closest tokens. 
    Otherwise, assigns a 0 to the token.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a verb of speech neighborhood.
    """
    vsn = [ 0 for e in s ]

    n = len(s)

    for i in range(n):
        if s[i][CORPUS_POS_INDEX] == 'VSAY':
            vsn[i] = 1
            if i-1 >= 0:
                vsn[i-1] = 1
            if i-2 >= 0:
                vsn[i-2] = 1
            if i+1 < n:
                vsn[i+1] = 1
            if i+2 < n:
                vsn[i+2] = 1

    return vsn

def applyLabel(q, pattern, text, dic, group, offset, offDic, label):
    p = re.compile(pattern)

    for m in re.finditer(p, text):
        #print(m.end(group) + offDic)
        q[ dic[m.end(group) + offDic] + offset ] = label

def convertNe(a, s):
    """
    Call the function convert with the parameters to translate the tokens
    in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, s, transIndex=3, valueList=["I-PER", "I-ORG"], label="#PO#")

def convertQuotationStart(a, qs):
    """
    Call the function convert with the parameters to translate the tokens
    in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, qs, transIndex=0, valueList=["S"], label="#QS#")

def convertProPess(a, s):
    """
    Translates the tokens in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, s, transIndex=1, valueList=["PROPESS"], label="#PPE#")

def convert(a, s, transIndex, valueList, label):
    """
    Given a 1D array a, a 2D sentence array s, sets
    a[i] to label, where s[transIndex] in labelList
    """
    for i in range(len(s)):
        if s[i][transIndex] in valueList:
            a[i] = label

def quoteBounds(s):
    """Creates a 1D array with Quotation Bounds indicators.

    Args:
        s: 2D array that represents a sentence in the BosqueQuotes format

    Returns:
        An 1D array that indicates if the i-th position 
        belongs to a quotation, marked with 'q'. If not,
        the position contains 'O'.
    """
    quote = ["-" for i in range(len(s))]

    for i in range(len(s)):
        if s[i][CORPUS_DEP_INDEX] != '-' and s[i][CORPUS_DEP_INDEX][:4] != 'Root':
            quote[i] = 'q'

    return quote

def detoken(a):
    """Detokenizes an array of tokens.

    Given an array a of tokens, it creates a text string with the tokens
    separated by space and a dictionary.

    This dicionary is usefull to translate from the
    indexes found by regexp in the text string

    Args:
        a: array of tokens

    Returns:
        A dicionary(k,v) where:
            v: original index of the token in the sentence
            k: index of the token in the string
    """
    text = " "
    #index = [2]
    index = [0]

    for i in range(len(a)):
        text = text + " " + a[i]
        index.append(i)
        for j in range(len(a[i])):
            index.append(i)
        #if i > 0:
            #index.append(index[i - 1] + 1 + len(a[i-1]))

    text = text + "\n"

    #dic = { index[i] : i for i in range(len(index)) }
    
    return text, index