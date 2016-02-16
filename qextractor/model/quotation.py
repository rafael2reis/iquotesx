# module quotation.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
quotation module - Functions to be used in the Structured Perceptron algorithm,
specifics for the Quotation Extraction Task.

"""
__version__="1.0"

import numpy as np

from qextractor.wis import wis

def argmax(w, e, loss=0):
    """Function that predicts the Quotation and the Author, given an example.

    Args:
        w: A list of weights
        e: A quotation.Example object
    Returns:
        A list of quotation.Row objects with the prediction.
    """

    tasks = []
    i = 0
    for r in e.x:
        l = 0
        if loss > 0 and not find(r, e.y):
            l = loss

        coref = w * np.array(r.coref.feat)
        t = wis.Task(r.quote.start, r.quote.end, np.sum(coref) + l, i)

        tasks.append(t)
        i += 1

    wmax, set_tasks = wis.schedule(tasks)

    result = convertTasks(set_tasks, e.x)

    return result

def find(r, y):
    """Auxiliary function that search for a quotation.Row r in the y set.

    Args:
        r: A quotation.Row object
        y: A list of quotation.Row objects
    Returns:
        The object in y with the same start time, end time and coref that r. None, otherwise.
    """
    start = r.quote.start
    end = r.quote.end
    coref = r.coref.label

    for x in y:
        if x.quote.start == start and x.quote.end == end and x.coref.label == coref:
            return x

    return None

def phi(e, y=None):
    """Calculates the weight of a Example.

    The weight will be the weight of each coref in the x or y list.

    Args:
        e: A quotation.Example object
        y: A list of quotation.Row objects
    Returns:
        The weight of the given example.
    """
    if not y:
        y = e.y

    if y:
        phi = np.zeros( (len(y[0].coref.feat)), dtype=int )
    else:
        phi = np.zeros( (len(e.x[0].coref.feat)), dtype=int )
        
    for r in y:
        if r.coref.label != "dummy":
            phi = phi + r.coref.feat

    return phi

def convertTasks(resultTasks, x):
    """Auxiliary function that convert a list of tasks
    in a list of quotation.Rows.

    Args:
        resultTasks: A list of Tasks objects
        x: A list of quotation.Row objects
    Returns:
        A list of quotation.Row objects.
    """
    conv = [ x[t.index] for t in resultTasks ]

    return conv


class Example:
    def __init__(self, x, y):
        self.x = x # List of Rows
        self.y = y # List of Rows

class Row:
    def __init__(self, quote, coref):
        self.quote = quote # A Quote
        self.coref = coref # A Coref

class Quote:
    def __init__(self, start, end):
        self.start = start # Start index of Quote
        self.end = end # End index of Quote

class Coref:
    def __init__(self, label, feat):
        self.label = label # Coref label
        self.feat = np.array([ int(e) for e in feat]) # Array of binary features
