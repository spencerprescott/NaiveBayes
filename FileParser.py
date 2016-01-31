class FileParser(object):
    @staticmethod
    def parse(file_name):
        reviews = open(file_name, "r")
        for review in reviews:
            # Loop through each review
            # First character is the category of the review: 1 or 0
            category = review[0]
            if "keyword" in review:
                pass


