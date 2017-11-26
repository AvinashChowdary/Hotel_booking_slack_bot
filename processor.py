from basics import basics
from analyzer import analyzer
from learnings import learnings
from hotel_scrapper import hotel_scrapper

class processor(object):
	def __init__(self):
		self.basics = basics()
		self.analyzer = analyzer()
		self.bot_doesnot_know = False
		self.next_is_place = False
		self.learnings = learnings()

	def process(self, command):
		reply = ""
		if self.bot_doesnot_know is False:
			if self.next_is_place is True:
				reply = self.getScrappedHotels(command)
				return reply
			if "find hotel" in command or "search hotel" in command or "hotel near" in command:
				target = "empty"
				if " in " in command:
					target = command.split(" in ",1)[1]
				if " at " in command:
					target = command.split(" at ",1)[1]
				if " near " in command:
					target = command.split(" near ",1)[1]
				if "me" in target or "empty" in target:
					next_is_place = True
					reply = "Sorry, could you specify the place to search hotels"
				else:
					reply = self.getScrappedHotels(target)
					return reply
			if command == "no":
				self.bot_doesnot_know = True
				reply = "Oops, Sorry about that. I am still learning. Could you rephrase and ask again?"
			else:
				reply = str(self.basics.respond(command))
				print(reply)
				if reply != "":
					return reply
				else:
					reply = "My Suggestion :: " +self.analyzer.analyze(command) + "\n"
					
			
		else:
			self.bot_doesnot_know = False
			self.learnings.learn(command)
			reply = "Sure, I will remember that"
			
				
		if self.bot_doesnot_know is False and reply != "Sure, I will remember that":
			reply = reply + "Are you satisfied with that response?"
		return reply

	def getScrappedHotels(self, value):
		hotels_dict = hotel_scrapper().scrape(value)
		reply = ""
		for x in hotels_dict:
			for y in hotels_dict[x]:
				reply = reply + y + " - " + hotels_dict[x][y]
				reply = reply + "\n"

		reply = reply + "These are the top results, would you like me to book a room for you ?\nPlease tell me the complete hotel name shown as above to proceed.\n Ask hotel : <hotelname>"
		return reply
