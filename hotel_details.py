from selenium import webdriver
import json
import string

class hotel_details(object):
	def __init__(self):
		self.driver = webdriver.Firefox()
	
	def scrape_details(self, url):
		detailsDict = dict()
		for i in range(1,2):
			self.driver.get(url)
 
			hotelAddresses = self.driver.find_elements_by_css_selector('span.hp_address_subtitle.jq_tooltip')
			hotelImages = self.driver.find_elements_by_css_selector('a.hotel_thumbs_sprite.change_large_image_on_hover.ephoto_info_collector')
			
			detailsDict[url] = {}
			detailsDict[url]['Address'] = hotelAddresses[0].text
			images = ""
			count = 0
			for hotelImage in zip(hotelImages):
				if(count <= 5):
					images = images + hotelImage[0].get_attribute('href') + "|"
					count+=1
			detailsDict[url]['Images'] = images
					
		return detailsDict
		
