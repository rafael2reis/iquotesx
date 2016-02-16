# module application.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
application module - Main module that trains and evaluate the model for the 
Quotation Extraction Task

"""

from qextractor.model import quotation
from qextractor.model import train
from qextractor.model import train_example
from qextractor.metrics import metrics
from pkg_resources import resource_filename

INPUT_TEST_FILE = resource_filename('qextractor', 'data/gen/qextractor_input_test.csv')

def main():
	"""Main function, that train and validade the model for the Quotation Extractor Task.

    """
    w = train.train()
    print(w)

    dataset = train_example.load(fileName=INPUT_TEST_FILE)

    precision, recall = metrics.validate(w, dataset=dataset, argmax=quotation.argmax)

    print("On the test set:\n")
    print("precision:", precision)
    print("recall:", recall)

if __name__ == '__main__':
    main()