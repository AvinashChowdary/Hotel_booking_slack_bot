from chatterbot import ChatBot

class logics(object):
		
	def __init__(self):
		self.bot = ChatBot(
			'Math Bot',
			trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
			logic_adapters=[
				'chatterbot.logic.MathematicalEvaluation',
				'chatterbot.logic.TimeLogicAdapter'
			],
			input_adapter="chatterbot.input.VariableInputTypeAdapter",
			output_adapter="chatterbot.output.OutputAdapter"
		)

	def respond(self,sentence):
		response = self.bot.get_response(sentence)
		return str(response)



	