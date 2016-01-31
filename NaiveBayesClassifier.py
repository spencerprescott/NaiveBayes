import sys
from FileParser import *


class NaiveBayesClassifier(object):
    def __init__(self, training_file, testing_file):
        super(NaiveBayesClassifier, self).__init__()
        self.training_set = FileParser.parse(training_file)
        self.testing_set = FileParser.parse(testing_file)

    def train(self):
        pass


def begin():
    classifier = NaiveBayesClassifier(sys.argv[1], sys.argv[2])
    classifier.train()

if len(sys.argv) == 3:
    begin()
else:
    print("Usage: python NaiveBayesClassifier.py TRAINING_SET.txt TESTING_SET.txt")
