from basics import basics
from hotel_scrapper import hotel_scrapper
from hotel_details import hotel_details
from db import bot_db
import json

class processor(object):
	def __init__(self):
		self.db = bot_db()
		self.basics = basics()
		self.next_anticipated = ""
		self.link = ""
		self.target = ""
		self.num_people = ""
		self.num_days = ""
		self.checkin_checkout = ""
		self.name = ""
		self.hotel = ""

	def process(self, command):
		
		reply = ""
		print("Anticipated : " + self.next_anticipated)
		
		if "place" in self.next_anticipated:
			reply = self.getScrappedHotels(command)
			self.next_anticipated = ""
			return reply

		if "another_hotel" in self.next_anticipated:
			if "yes" in command or "yeah" in command or "yup" in command or "yep" in command:
				reply = "Please provide a link of the hotel or ask : search hotel in <city/place>"
				self.next_anticipated = ""
				return reply
			elif "no" in command or "nope" in command or "nah" in command:
				reply = "Why don't we start over, ask : search hotel in <city/place>"
				self.next_anticipated = ""
				self.name = ""
				self.link = ""
				self.target = ""
				self.num_days = ""
				self.num_people = ""
				self.checkin_checkout = ""
				return reply

		if "num_people" in self.next_anticipated:
			if command.isdigit():
				reply = "Great ! could you specify the number of days you would like to stay ?"
				self.num_people = command
				self.next_anticipated = "num_days"
				return reply
			else:
				reply = "could you please specify the number of people in correct format ?"
				self.next_anticipated = "num_people"
				return reply
		
		if "num_days" in self.next_anticipated:
			if command.isdigit():
				reply = "Sure ! can you specify the checkin and check out dates as well"
				self.num_days = command
				self.next_anticipated = "dates"
				return reply
			else:
				reply = "could you please specify the dates in correct format ?"
				self.next_anticipated = "num_days"
				return reply

		if "dates" in self.next_anticipated:
			if command:
				reply = "Great ! do you confirm booking ?"
				self.checkin_checkout = command
				self.next_anticipated = "confirmation"
				return reply
		
		if "confirmation" in self.next_anticipated:
			if "yes" in command or "yeah" in command or "yup" in command or "yep" in command:
				dataDict = dict()
				dataDict[self.name] = {}
				dataDict[self.name]['name'] = self.name
				dataDict[self.name]['place'] = self.target
				dataDict[self.name]['hotel'] = self.hotel
				dataDict[self.name]['link'] = self.link
				dataDict[self.name]['num_people'] = self.num_people
				dataDict[self.name]['num_days'] = self.num_days
				dataDict[self.name]['checkin_checkout'] = self.checkin_checkout
				json_data = json.dumps(dataDict)
				print(json_data)
				print(str(json_data))
				id = self.db.write(json_data)
				reply = "Great ! Your booking has been made\nHere are the details\n"
				reply = reply + "Booking on the Name : " + self.name + "\n"
				reply = reply + "at " + self.target.title() + "\n"
				reply = reply + "in " + self.hotel.title() + "\n"
				reply = reply + "for " + self.num_people.title() + "persons\n"
				reply = reply + "for " + self.num_days.title() + "days\n"
				reply = reply + "from " + self.checkin_checkout.title() + "\n"
				reply = reply + "Transaction ID : " + str(id) + "\n"
				reply = reply + "Thanks for making a booking with us, enjoy your stay."
				self.next_anticipated = ""
				self.name = ""
				self.link = ""
				self.target = ""
				self.num_days = ""
				self.num_people = ""
				self.checkin_checkout = ""
				return reply
			elif "no" in command or "nope" in command or "nah" in command:
				reply = "Would you like to start again ? Ask find hotel in <city/place>"
				self.next_anticipated = ""
				self.name = ""
				self.link = ""
				self.target = ""
				self.num_days = ""
				self.num_people = ""
				self.checkin_checkout = ""
				return reply

		if "acceptance" in self.next_anticipated:		
			if "yes" in command or "yeah" in command or "yup" in command or "yep" in command:
				if self.link:
					reply = ""
					reply = "For how many people would you like to book ?"
					self.next_anticipated = "num_people"
					return reply
			elif "no" in command or "nope" in command or "nah" in command:
				reply = "Sorry, Would you like to book for another hotel ?"
				self.next_anticipated = "another_hotel"
				return reply
			else:
				reply = "Would you like to begin again ? Try asking to search hotel in <City/Area>"
				self.next_anticipated = ""
				self.name = ""
				self.link = ""
				self.target = ""
				self.num_days = ""
				self.num_people = ""
				self.checkin_checkout = ""
				return reply
				
		if "https://www.booking.com/hotel/" in command:
			url = command[1:len(command) - 1]
			self.link = url
			temp = url.split("https://www.booking.com/hotel/us/", 1)[1]
			tmp = temp.replace(".html", "")
			nme = tmp.replace("-", " ")
			self.name = nme
			self.next_anticipated = "acceptance"
			reply = self.getHotelDetails(url)
			return reply
		
		if "find hotel" in command or "search hotel" in command or "hotel near" in command:
			if " in " in command:
				self.target = command.split(" in ",1)[1]
			if " at " in command:
				self.target = command.split(" at ",1)[1]
			if " near " in command:
				self.target = command.split(" near ",1)[1]
			if "me" in self.target:
				self.next_anticipated = "link"
				reply = "Sorry, could you specify the place to search hotels"
			else:
				reply = self.getScrappedHotels(self.target)
				return reply
	
		reply = str(self.basics.respond(command))
		print(reply)
		if reply != "":
			return reply
		else:
			reply = "Sorry, my I am afraid that I did not understand. Could you please rephrase and try !!"

	def getScrappedHotels(self, value):
		if value:
			hotels_dict = hotel_scrapper().scrape(value)
			reply = ""
			if hotels_dict:
				for x in hotels_dict:
					for y in hotels_dict[x]:
						reply = reply + y + " - " + hotels_dict[x][y]
						reply = reply + "\n"

				reply = reply + "These are the top results, would you like me to book a room for you ?\nPlease give me the complete hotel link shown as above to proceed."
				return reply
			else:
				reply = "Could you be more specific about the location ?"
				return reply
		else:
			reply = "Could you please spcify a place so that I can search hotels nearby !!"
			return reply

	def getHotelDetails(self, link):
		details_dict = hotel_details().scrape_details(link)
		reply = ""
		reply = reply + "Address : " + details_dict[link]['Address'] + "\n"
		images = details_dict[link]['Images'].split('|')
		reply = reply + "Some Pictures of the place : \n"
		for image in images:
			reply = reply + image + "\n"
		reply = reply + "Do you wish to continue with booking ?"
		return reply
