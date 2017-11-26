from understanding import understanding
import db

class learnings(object):

	def __init__(self):
		self.db = db.bot_db()
		self.understanding = understanding()

	def learn(self, sentence):
		reply = {}
		reply = self.understanding.understand(sentence)
		self.db.insert(reply)