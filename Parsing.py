import re
import string

class ReviewParser(object):
    def __init__(self):
        super(ReviewParser, self).__init__()


    @staticmethod
    def parse_for_training(reviews, word_count):
        negations = ["not", "can't", "cannot", "shouldn't"]
        while True:
            review = reviews.readline()
            review = review.rstrip()
            if not review:
                break
            # Loop through each review
            # First character is the category of the review: 1 or 0
            category = int(review[0])
            # Make review lowercase
            review = review.lower()
            # Remove punctuation
            review = review.translate(string.maketrans("",""), string.punctuation)
            # Remove html tags
            review = re.sub("<[^<]+?>", "", review)
            # String => Array
            words = review.split()
            word_count[category].append({})
            for i in range(0, len(words)):
                word = words[i]
                if i == 0 or (i-1 > 0 and words[i-1] not in negations):
                    if word in word_count[category][-1].keys():
                        word_count[category][-1][word] += words.count(word)
                    else:
                        word_count[category][-1][word] = words.count(word)
                elif i == 0 or (i-1 > 0 and words[i-1] in negations):
                    word = words[i-1] + " " + words[i]
                    if word in word_count[category][-1].keys():
                        word_count[category][-1][word] += words.count(word)
                    else:
                        word_count[category][-1][word] = words.count(word)
        reviews.close()

    @staticmethod
    def parse_for_labeling(reviews):
        word_lists = []
        while True:
            review = reviews.readline()
            review = review.rstrip()
            if not review:
                break
            # Loop through each review
            # First character is the category of the review: 1 or 0
            category = int(review[0])
            # Make review lowercase
            review = review.lower()
            # Remove punctuation
            review = review.translate(string.maketrans("",""), string.punctuation)
            # Remove html tags
            review = re.sub("<[^<]+?>", "", review)
            # String => Array
            words = review.split()
            word_lists.append(
                {
                    "real_category" : category,
                    "words" : words
                }
            )
        reviews.close()
        return word_lists