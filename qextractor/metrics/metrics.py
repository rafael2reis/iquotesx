# module metrics.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
metrics module - Functions to evaluate the quality and performance of a model

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

def validate(w, dataset, argmax):
    """Validates a model w based on a dataset.

    Args:
        w: The model already trainned
        dataset: The data to be validated
        argmax: The function used to predict
    Returns:
        A tuple composed by the metrics Precision and Recall
    """
    corr = 0.0
    incorr = 0.0
    corrD = 0.0 # Correct Dummy
    incorrD = 0.0 # Incorrect Dummy
    quot = 0.0 # Num of real quotations

    for e in dataset:
        predict = argmax(w, e)

        y = e.y
        quot += len(y)
        for r in predict:
            a = search(r, y)

            if not a:
                if r.coref.label == "dummy":
                    corrD += 1
                else:
                    incorrD += 1
            else:
                if r.coref.label == a.coref.label:
                    corr += 1
                else:
                    incorr += 1

    precision = (corr + corrD)/(corr + corrD + incorr + incorrD)
    recall = corr/quot

    return precision, recall

def show(w, train, test, argmax, epoch):
    """Print the metrics Precision and Recall for the 
        train and test set.

    Args:
        w: The model already trainned
        train: The train dataset
        test: The test dataset
        argmax: The function used to predict
        epoch: An index to be displayed at the line beginning
    """
    ptra, rectra = validate(w, train, argmax)
    ptes, rectes = validate(w, test, argmax)

    print(epoch.ljust(3), str(ptra).ljust(20), str(rectra).ljust(20), str(ptes).ljust(20), str(rectes).ljust(20))

def search(r, y):
    """Auxiliary function that search for a quotation.Row in the y set
        that has the same start and end times of r.

    Args:
        r: A quotation.Row object
        y: A list of quotation.Row objects
    Returns:
        The object in y with the same start and end times that r. None, otherwise.
    """
    start = r.quote.start
    end = r.quote.end

    for x in y:
        if x.quote.start == start and x.quote.end == end:
            return x

    return None