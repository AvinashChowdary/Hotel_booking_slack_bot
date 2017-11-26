from understanding import understanding
from matcher import matcher


class analyzer(object):
    def __init__(self):
        self.matcher = matcher();
        self.understanding = understanding();

    def analyze(self, command):
        knowledge = understanding.understand(command)
        return matcher.match(knowledge)