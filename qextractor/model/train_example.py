# module train_example.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
train_example module - Load the train examples from file

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import csv

from qextractor.model.quotation import *
from pkg_resources import resource_filename

INPUT_FILE = resource_filename('qextractor', 'data/gen/qextractor_input.csv')

def load(fileName=None):
	"""Load a list of quotation.Examples from a CSV file.

    Args:
        fileName: A CSV file in the Example format, wrote by the Base Line System.
    Returns:
        A list of quotation.Examples.
    """
	if not fileName:
		fileName = INPUT_FILE

	with open(fileName, newline='') as csvfile:
		sreader = csv.reader(csvfile, delimiter=';')
		
		iPrev = 0
		i = 0

		examples = []
		x = []
		y = []

		for row in sreader:
			i = int(row[0])
			if i != iPrev:
				examples.append( Example(x, y) )
				x, y = [], []

			quote = Quote(int(row[2]), int(row[3]))
			coref = Coref(label = row[4], feat = row[5:len(row)])
			
			r = Row(quote, coref)

			if row[1] == 'x':
				x.append(r)
			else:
				y.append(r)

			iPrev = i

		ex = Example(x, y)
		examples.append(ex)

	return examples