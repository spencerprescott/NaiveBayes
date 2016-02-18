class DataModel(object):
    """
    Class holding P(C=c) and all the P(X=x) and P(X=x|C=c) where C = ["positive", "negative"], and X = all words in reviews
    """
    def __init__(self, num_positive_reviews, num_negative_reviews):
        super(DataModel, self).__init__()
        self.probability_is_positive_review = float(num_positive_reviews) / float(num_negative_reviews + num_positive_reviews)
        self.probability_is_negative_review = float(num_negative_reviews) / float(num_negative_reviews + num_positive_reviews)
        self.word_probabilites = {
            "positive" : {}, # P(X=x | C=positive)
            "negative" : {}  # P(X=x | C=negative)
        }

    def generate_word_probabilites(self, positive_review_word_count, negative_review_word_count):
        """
        Loops through the word counts for positive and negative reviews and generates P(X=x|C=c)te
        :param word_sums:
        :return None:
        """
        word_sums = {
            "positive" : {},
            "negative" : {}
        }
        # First get the frequency of each word and separate by positive and negative reviews
        for positive_review_words, negative_review_words in zip(positive_review_word_count, negative_review_word_count):
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
        # Get conditional probability for positive first
        for word in word_sums["positive"]:
            positive_count = word_sums["positive"][word]
            negative_count = 0
            if word in word_sums["negative"]:
                negative_count = word_sums["negative"][word]
            # P(x|c) = n_k / n
            total = positive_count + negative_count
            if total > 0:
                self.word_probabilites["positive"][word] = float(positive_count) / total
                self.word_probabilites["negative"][word] = float(negative_count) / total

        # Do negative next, but only words that were not in positive
        for word in word_sums["negative"]:
            if word not in self.word_probabilites["positive"]:
                self.word_probabilites["negative"][word] = 1
                self.word_probabilites["positive"][word] = 0
