from selenium import webdriver
import json

class hotel_scrapper(object):
	def __init__(self):
		self.driver = webdriver.Firefox()
	
	def scrape(self, city):
		hotelsDict = dict()
		k = 0;
		for i in range(1,2):
			url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmcgV1c19jYYgBAZgBMbgBB8gBDNgBAegBAfgBApICAXmoAgM;sid=9428a9c8de49fd886b9075dd0822efd9;class_interval=1&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=" + city + "&ss_all=0&ssb=empty&sshis=0&"
			self.driver.get(url)
 
			hotelUrls = self.driver.find_elements_by_css_selector('a.hotel_name_link.url')
			hotelNames = self.driver.find_elements_by_css_selector('span.sr-hotel__name')
			hotelRatings = self.driver.find_elements_by_css_selector('span.review-score-badge')
			hotelDetails = self.driver.find_elements_by_css_selector('span.distfromdest.jq_tooltip')
			hotelDescs = self.driver.find_elements_by_css_selector('div.hotel_desc')

			for hotelurl,hotelname,hotelrating,hoteldetail,hoteldesc in zip(hotelUrls,hotelNames,hotelRatings,hotelDetails,hotelDescs):
				#get hotel name
				name = hotelname.text
				# get url
				url = hotelurl.get_attribute('href').split('?')[0]
				# get rating
				rating = hotelrating.text
				hotelsDict[str(k)] = {}
				hotelsDict[str(k)]['Link'] = url
				hotelsDict[str(k)]['Name'] = name.lower()
				hotelsDict[str(k)]['Rating'] = rating
				hotelsDict[str(k)]['Location'] = hoteldetail.text
				hotelsDict[str(k)]['Description'] = hoteldesc.text
				k = k+1

		return hotelsDict
		
