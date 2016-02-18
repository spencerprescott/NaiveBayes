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
        review_word_counts = [[], []]
        review_word_counts[0] = word_count[0]
        review_word_counts[1] = word_count[1]

        #self.remove_stop_words(review_word_counts)
        self.create_model(review_word_counts)
        end = time.clock()
        self.time_to_train_string = str(end - start) + " seconds (training)"

    def classify(self):
        start = time.clock()
        reviews = open(self.testing_file, "r")
        parsed_reviews = ReviewParser.parse_for_labeling(reviews)
        classified_reviews = self.classify_reviews(parsed_reviews)
        self.get_classification_accuracy(classified_reviews)
        self.run_classification_on_training()
        end = time.clock()
        self.time_to_label_string = str(end - start) + " seconds (labeling)"

        print(self.time_to_train_string)
        print(self.time_to_label_string)
        print(self.training_accuracy_string)
        print(self.classification_accuracy_string)

    # Private

    # Training
    def create_model(self, review_word_counts):
        self.model = DataModel(len(review_word_counts[1]), len(review_word_counts[0]))
        word_sums = self.get_sum_of_words(review_word_counts)
        self.model.generate_word_probabilites(word_sums)

    def get_sum_of_words(self, review_word_counts):
        word_sums = {
            "positive" : {},
            "negative" : {}
        }
        for positive_review_words, negative_review_words in zip(review_word_counts[1], review_word_counts[0]):
            for word in positive_review_words:
                if word in word_sums["positive"]:
                    word_sums["positive"][word] += positive_review_words[word]
                else:
                    word_sums["positive"][word] = positive_review_words[word]
            for word in negative_review_words:
                if word in word_sums["negative"]:
                    word_sums["negative"][word] += negative_review_words[word]
                else:
                    word_sums["negative"][word] = negative_review_words[word]
        return word_sums

    def remove_stop_words(self, review_word_counts):
        for positive_review_word_count, negative_review_word_count in zip(review_word_counts[1], review_word_counts[0]):
            ordered_word_count_positive = sorted(positive_review_word_count, key=positive_review_word_count.get, reverse=True)
            ordered_word_count_negative = sorted(negative_review_word_count, key=negative_review_word_count.get, reverse=True)

    # Classification

    def classify_reviews(self, parsed_reviews):
        classified_reviews = []
        for review_info in parsed_reviews:
            prob_neg = math.log10(self.model.probability_is_negative_review)
            prob_pos = math.log10(self.model.probability_is_positive_review)
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
