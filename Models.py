class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.data = self.construct_data()

    # Initially constructs data for model
    def construct_data(self):
        return {}

class Positive(Model):
    def __init__(self):
        super(Positive, self).__init__()

    def construct_data(self):
        return {
            "i like" : 0,
            "pleased" : 0,
            "happy" : 0,
            "enjoy" : 0
        }

class Negative(Model):
    def __init__(self):
        super(Negative, self).__init__()

    def construct_data(self):
        return {
            "not happy" : 0,
            "sad" : 0,
            "bad" : 0,
            "avoid" : 0
        }