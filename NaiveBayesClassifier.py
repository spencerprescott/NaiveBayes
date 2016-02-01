import sys
from Parsing import *
import pickle
import os.path

class NaiveBayesClassifier(object):
    def __init__(self, training_file, testing_file):
        super(NaiveBayesClassifier, self).__init__()
        self.training_file = training_file
        self.testing_file = testing_file
        self.data_models = [{}, {}]

    def train(self, use_cached=False):
        reviews = open(self.training_file, "r")
        if use_cached == True:
            if os.path.exists("cache.pickle"):
                with open("cache.pickle", "rb") as handle:
                    word_count = pickle.load(handle)
            else:
                word_count = [{}, {}]
                ReviewParser.parse(reviews, word_count)
        else:
            word_count = [{}, {}]
            ReviewParser.parse(reviews, word_count)

        # Modifies word_count

        self.data_models[0] = word_count[0]
        self.data_models[1] = word_count[1]
        # Cache data models
        with open("cache.pickle", "wb") as handle:
            pickle.dump(self.data_models, handle)

        print(self.data_models[0]["love"])
        print(self.data_models[1]["love"])

    def classify(self):
        reviews = open(self.testing_file, "r")
        for review in reviews:
            pass


if len(sys.argv) == 3:
    classifier = NaiveBayesClassifier(sys.argv[1], sys.argv[2])
    classifier.train(use_cached=True)
else:
    print("Usage: python NaiveBayesClassifier.py <training_set>.txt <testing_set>.txt")
