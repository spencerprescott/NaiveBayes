import time
import re

class ReviewParser(object):
    def __init__(self):
        super(ReviewParser, self).__init__()

    @staticmethod
    def get_filler_words():
        return [
            "the", "a", "if", "in", "this", "to", "of",
            "and", "to", "that", "was", "on", "it", "but",
            "be", "you", "with", "as", "for", "they", "her",
            "him", "one", "so", "from", "who", "or", "all", "just",
            "about", "some", "there", "what", "i", "his", "she", "is",
            "are", "he"
        ]

    @staticmethod
    def parse(reviews, word_count):
        negations = ["not", "can't", "cannot", "shouldn't"]
        filler_words = ReviewParser.get_filler_words()
        start = time.clock()
        for review in reviews:
            # Loop through each review
            # First character is the category of the review: 1 or 0
            category = int(review[0])
            review = review.lower()
            review = re.sub("<[^<]+?>", "", review)
            words = review.split()
            seen_words = []
            for i in range(0, len(words)):
                word = words[i]
                if "." in word:
                    word = re.sub(".", " ", word)
                elif "," in word:
                    word = re.sub(",", " ", word)
                if word not in seen_words and word not in filler_words:
                    if i == 0 or (i-1 > 0 and words[i-1] not in negations):
                        if word in word_count[category].keys():
                            word_count[category][word] += words.count(word)
                        else:
                            word_count[category][word] = words.count(word)
                        seen_words.append(word)
        end = time.clock()
        print(str(end - start) + " seconds (training)")
