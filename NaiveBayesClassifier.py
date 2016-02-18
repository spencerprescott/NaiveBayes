import sys
from Parsing import *
import time
from DataModel import *
import math

class NaiveBayesClassifier(object):
    def __init__(self, training_file, testing_file):
        super(NaiveBayesClassifier, self).__init__()
        self.training_file = training_file
        self.testing_file = testing_file
        self.model = None
        self.time_to_train_string = ""
        self.time_to_label_string = ""
        self.classification_accuracy_string = ""
        self.training_accuracy_string = ""

    def train(self):
        start = time.clock()
        reviews = open(self.training_file, "r")
        word_count = [[], []]
        # Populate word_count array with 2 arrays, word_count[0] is for the 0 reviews and word_count[1] is
        # for the 1 reviews. Each element of those arrays contain a dictionary for the word count for a specific review
        ReviewParser.parse_for_training(reviews, word_count)

        self.create_model(word_count)
        end = time.clock()
        self.time_to_train_string = str(int(end - start)) + " seconds (training)"

    def classify(self):
        start = time.clock()
        reviews = open(self.testing_file, "r")
        parsed_reviews = ReviewParser.parse_for_labeling(reviews)
        classified_reviews = self.classify_reviews(parsed_reviews)
        # This method will print the labels followed by a newline
        self.get_classification_accuracy(classified_reviews)
        self.run_classification_on_training()
        end = time.clock()
        self.time_to_label_string = str(int(end - start)) + " seconds (labeling)"

        # Print all the required timing and accuracy
        print(self.time_to_train_string)
        print(self.time_to_label_string)
        print(self.training_accuracy_string)
        print(self.classification_accuracy_string)

    # Helper Methods

    # Training
    def create_model(self, review_word_counts):
        self.model = DataModel(len(review_word_counts[1]), len(review_word_counts[0]))
        self.model.generate_word_probabilites(review_word_counts[1], review_word_counts[0])

    # Classification
    def classify_reviews(self, parsed_reviews):
        classified_reviews = []
        for review_info in parsed_reviews:
            prob_neg = math.log10(self.model.probability_is_negative_review)
            prob_pos = math.log10(self.model.probability_is_positive_review)
            # Use the sum of logs to deal with really small numbers log(P(C=c)) + sum_i(P(X=x_i|C=c))
            for word in review_info["words"][1:]:
                if word in self.model.word_probabilites["negative"]:
                    conditional_neg = self.model.word_probabilites["negative"][word]
                    if conditional_neg > 0:
                        prob_neg += math.log10(conditional_neg)
                if word in self.model.word_probabilites["positive"]:
                    conditional_pos = self.model.word_probabilites["positive"][word]
                    if conditional_pos > 0:
                        prob_pos += math.log10(conditional_pos)
            classified_reviews.append(
                {
                    "real_category" : int(review_info["real_category"]),
                    "calculated_category" : 1 if prob_pos > prob_neg else 0
                }
            )
        return classified_reviews

    def get_classification_accuracy(self, classified_reviews):
        num_correct = 0
        total = 0
        for review_classification in classified_reviews:
            total += 1
            print(review_classification["calculated_category"])
            if review_classification["real_category"] == review_classification["calculated_category"]:
                num_correct += 1

        classification_accuracy = float(num_correct) / float(total)
        self.classification_accuracy_string = str(classification_accuracy) + " (testing)"

    def get_training_accuracy(self, classified_reviews):
        num_correct = 0
        total = 0
        for review_classification in classified_reviews:
            total += 1
            if review_classification["real_category"] == review_classification["calculated_category"]:
                num_correct += 1

        training_accuracy = float(num_correct) / float(total)
        self.training_accuracy_string = str(training_accuracy) + " (training)"

    def run_classification_on_training(self):
        reviews = open(self.training_file, "r")
        parsed_reviews = ReviewParser.parse_for_labeling(reviews)
        classified_reviews = self.classify_reviews(parsed_reviews)
        self.get_training_accuracy(classified_reviews)



if len(sys.argv) == 3:
    classifier = NaiveBayesClassifier(sys.argv[1], sys.argv[2])
    classifier.train()
    classifier.classify()
else:
    print("Usage: python NaiveBayesClassifier.py <training_set>.txt <testing_set>.txt")
