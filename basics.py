from chatterbot import ChatBot

class basics(object):

	def __init__(self):
		self.bot = ChatBot(
			'Hotel Booking Bot',
			trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
	  	)

		# self.bot.train('chatterbot.corpus.english.greetings')
		self.bot.train('chatterbot.corpus.english.conversations')
		# self.bot.train('chatterbot.corpus.english.ai')
		# self.bot.train('chatterbot.corpus.english.computers')
		# self.bot.train('chatterbot.corpus.english.emotion')
		# self.bot.train('chatterbot.corpus.english.history')
		# self.bot.train('chatterbot.corpus.english.humor')
		# self.bot.train('chatterbot.corpus.english.literature')
		# self.bot.train('chatterbot.corpus.english.money')
		# self.bot.train('chatterbot.corpus.english.psychology')
		# self.bot.train('chatterbot.corpus.english.science')
		# self.bot.train('chatterbot.corpus.english.sports')
		# self.bot.train('chatterbot.corpus.english.trivia')

	def respond(self,sentence):
		response = self.bot.get_response(sentence)
		return response