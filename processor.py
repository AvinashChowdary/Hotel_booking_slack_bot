from basics import basics
from hotel_scrapper import hotel_scrapper
from hotel_details import hotel_details
from db import bot_db
import json
import time
import datetime
import struct
from random import randint
from logics import logics


class processor(object):
	def __init__(self):
		self.db = bot_db()
		self.basics = basics()
		self.logics = logics()
		self.next_anticipated = ""
		self.link = ""
		self.target = ""
		self.num_people = ""
		self.num_days = ""
		self.checkin_checkout = ""
		self.name = ""
		self.hotel = ""
		self.hotels_dict = dict()

	def getID(self):
		now = datetime.datetime.now()
		stamp = time.mktime(now.timetuple())
		binarydatetime = struct.pack('<L', int(stamp))
		bts = struct.unpack('<L', binarydatetime)[0]
		return bts

	def process(self, command):
		
		reply = ""
		print("Anticipated : " + self.next_anticipated)

		if "cancel booking" in command:
			reply = "I can do that for you, please provide me with the transaction ID"
			self.next_anticipated = "cancel_booking"
			return reply

		if "cancel_booking" in self.next_anticipated and command:
			if command.isdigit():
				reply = "Your booking with Transaction ID " + command + " has been cancelled."
				self.db.delete_booking(command)
				self.next_anticipated = ""
				return reply
			else:
				reply = "Please enter valid Transaction ID"
				self.next_anticipated = "cancel_booking"
				return reply

		if "can you show me bookings" in command or "my bookings" in command or "show bookings" in command or "my booking" in command:
			self.next_anticipated = "booking_key"
			reply = "Could you please provide me Transaction ID so that I can look up"
			return reply

		if "booking_key" in self.next_anticipated:
			booking = self.db.get_booking(command)
			response = json.loads(booking)
			if response:
				reply = "Great ! Here is your booking\n"
				reply = reply + "Booking on Name : " + response[0]['name'].title() + "\n"
				reply = reply + "at " + response[0]['hotel'].title() + "\n"
				reply = reply + "for " + response[0]['num_people'].title() + " persons\n"
				reply = reply + "for " + response[0]['num_days'] .title()+ " days\n"
				reply = reply + "from " + response[0]['checkin_checkout'].title() + "\n"
				reply = reply + "Transaction ID : " + response[0]['booking_id'] + "\n"
				self.next_anticipated = ""
				self.name = ""
				self.link = ""
				self.target = ""
				self.num_days = ""
				self.num_people = ""
				self.checkin_checkout = ""
				return reply
			else:
				reply = "Sorry, I couldn't find any bookings with the given ID"
				self.next_anticipated = ""
				return reply
		
		if "place" in self.next_anticipated:
			reply = self.getScrappedHotels(command)
			self.next_anticipated = ""
			return reply

		if "another_hotel" in self.next_anticipated:
			if "yes" in command or "yeah" in command or "yup" in command or "yep" in command:
				reply = "Please provide name of the hotel or ask : search hotel in <city/place>"
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
				total = 136
				if int(self.num_days) > 2 and int(self.num_people) > 2:
					total = randint(400, 600)
				else:
					total = randint(120, 300)
				reply = "Your total would be : $" + str(total) + "\n"
				reply = reply + "What would be a good name to make the booking ?"
				self.checkin_checkout = command
				self.next_anticipated = "name"
				return reply
		
		if "name" in self.next_anticipated:
			if command:
				self.name = command
				reply = "Great ! do you confirm booking ?"
				self.next_anticipated = "confirmation"
				return reply	
		
		if "confirmation" in self.next_anticipated:
			if "yes" in command or "yeah" in command or "yup" in command or "yep" in command:
				dataDict = dict()
				dataDict = {}
				dataDict['name'] = self.name
				dataDict['hotel'] = self.hotel
				dataDict['link'] = self.link
				dataDict['num_people'] = self.num_people
				dataDict['num_days'] = self.num_days
				dataDict['checkin_checkout'] = self.checkin_checkout
				id = self.getID()
				dataDict['booking_id'] = str(id)
				json_data = json.dumps(dataDict)
				print(json_data)
				print(str(json_data))
				self.db.write(json_data)
				reply = "Great ! Your booking has been made\nHere are the details\n"
				reply = reply + "Booking on Name : " + self.name.title() + "\n"
				reply = reply + "at " + self.hotel.title() + "\n"
				reply = reply + "for " + self.num_people.title() + " persons\n"
				reply = reply + "for " + self.num_days.title() + " days\n"
				reply = reply + "from " + self.checkin_checkout.title() + "\n"
				reply = reply + "Transaction ID : " + str(id) + "\n"
				reply = reply + "Thanks for making a booking with us, enjoy your stay.\n"
				reply = reply + "* You can always view your bookings. Ask : <my bookings>"
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
			self.hotel = nme
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
	
		for x in self.hotels_dict:
			if command in self.hotels_dict[x]['Name']:
				href = self.hotels_dict[x]['Link']
				self.hotel = self.hotels_dict[x]['Name']
				print(href)
				self.link = href
				self.next_anticipated = "acceptance"
				reply = self.hotel.title() + "\n"
				reply = reply + "For more details refer to : " + href + "\n"
				reply = reply + self.getHotelDetails(href)
				return reply
		
		if "time" in command and "what" in command:
			reply = self.logics.respond(command)
			return reply
			
		if "+" in command or "-" in command or "*" in command or "/" in command:
			for i in command:
				if i.isdigit():
					reply = self.logics.respond(command)
					return reply

		reply = str(self.basics.respond(command))
		if reply != "":
			return reply
		else:
			reply = "Sorry, my I am afraid that I did not understand. Could you please rephrase and try !!"

	def getScrappedHotels(self, value):
		self.hotels_dict = dict()
		if value:
			self.hotels_dict = hotel_scrapper().scrape(value)
			reply = ""
			if self.hotels_dict:
				for x in self.hotels_dict:
					for y in self.hotels_dict[x]:
						if "https://www.booking.com" in self.hotels_dict[x][y]:
							pass
						else:
							reply = reply + y + " - " + self.hotels_dict[x][y].title()
							reply = reply + "\n"
					reply = reply + "\n"
				reply = reply + "\nThese are the top results, would you like me to book a room for you ?\nPlease give me the complete hotel name shown as above to proceed."
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
		reply = reply + "Some pictures of the place : \n"
		for image in images:
			reply = reply + image + "\n"
		reply = reply + "Do you wish to continue with booking ?\n"
		return reply
