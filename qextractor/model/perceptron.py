# module perceptron.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
perceptron module - Perceptron algorithm that creates the model.

"""
__version__="1.0"

import numpy as np
from qextractor.metrics import metrics

def structured(w, train, test, epochs, argmax, phi):
    """Structured Perceptron algorithm.

    Args:
        w: A list of weights
        train: The train data set
        test: The test data set
        epochs: How many times the entiry train dataset will be looped
        argmax: The function that does the prediction
        phi: The function that computes the weight of a given example
    Returns:
        The model trained.
    """
    i = 0
    while i < epochs:
        for e in train:
            yp =  argmax(w, e, loss=400)
            w = w + phi(e) - phi(e, yp)
        i += 1

        if test:
            metrics.show(w=w, train=train, test=test, argmax=argmax, epoch=str(i))
    return w
