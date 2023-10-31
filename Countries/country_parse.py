class country:
    def __init__(self, name, topic, time_length):
        self.title = name
        self.topic = topic
        self.time_start = time_length[0]
        self.time_end = time_length[1]
        self.categories = []
        self.actors = []
        self.events = {}
        