# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
# Mac Users
	# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	# browser = Browser('chrome', **executable_path, headless=False)

# Windows Users
# Choose the executable path to driver (Windows)
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():

	# Mission to Mars Dictionary
	mars_data = {}

	# **********************************
	# Nasa Mars News
	# **********************************
	browser = init_browser()

	# URL of page to be scraped
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	time.sleep(3)
	# Create BeautifulSoup object; parse with 'html.parser'
	html = browser.html
	soup = bs(html, 'html.parser')

	# scrape the article for first New Title 
	title = soup.find('div', class_='content_title').find('a').text

	# scrape the article teaser paragraph
	first_pp = soup.find('div', class_='article_teaser_body').get_text()


	browser.quit()

	# **********************************
	# JPL Mars Space Images - Featured Image
	# **********************************

	browser = init_browser()

	# Visit the url for JPL Featured Space Image here. https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
	image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url)
	time.sleep(3)
	# Use splinter to navigate the site and find the image url for the current Featured Mars Image 
	# Make sure to find the image url to the full size .jpg image.
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(3)
	image_html = browser.html
	image_soup = bs(image_html, 'html.parser')
	find_image_url = image_soup.find('img', class_='fancybox-image')['src']
	featured_image_url = f'https://www.jpl.nasa.gov{find_image_url}'

	browser.quit()


	# **********************************
	# Mars Weather
	# **********************************

	browser = init_browser()

	# Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(weather_url)
	time.sleep(3)
	# Save the tweet text for the weather report as a variable called mars_weather
	weather_html = browser.html
	weather_soup = bs(weather_html, 'html.parser')

	tweets = weather_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

	# loop to find the first tweet
	for tweet in tweets:
	    weather = tweet.get_text()
	    
	    if "InSight sol" in weather:
	        mars_weather = weather
	        break

	browser.quit()

	# **********************************
	# Mars Facts
	# **********************************

	browser = init_browser()

	# Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including:
	# Diameter, Mass, etc.
	facts_url = 'https://space-facts.com/mars/'
	browser.visit(facts_url)
	time.sleep(3)
	# Use Pandas to convert the data to a HTML table string
	mars_read = pd.read_html(facts_url)
	mars_facts = pd.DataFrame(mars_read[0])
	mars_facts.columns = ['Description', 'Value']

	mars_html = mars_facts.to_html(index=False)

	browser.quit()

	# **********************************
	# Mars Hemispheres
	# **********************************

	browser = init_browser()

	hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemi_url)
	time.sleep(3)
	# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
	# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title
	# create empty list for the hemispheres
	mars_hemi = []

	urls = browser.find_by_css('a.product-item h3')

	for i in range(len(urls)):
	    # Use a Python dictionary to store the data using the keys img_url and title
	    hemi_dict = {}
	    
	    browser.find_by_css('a.product-item h3')[i].click()
	    time.sleep(1)
	    hemi_url = browser.find_link_by_text('Sample').first
	    # Store the data using the keys img_url and title
	    hemi_dict['img_url'] = hemi_url['href']
	    hemi_dict['title'] = browser.find_by_css('h2.title').text.strip(' Enhanced')
	    mars_hemi.append(hemi_dict)

	    browser.back()

	browser.quit()

    # Save scraped data into dictionary
	mars_data = {"title":title,
				"first_pp":first_pp,
				"featured_image_url":featured_image_url,
				"weather":weather,
				"mars_html":mars_html,
				"mars_hemi":mars_hemi
	            }
    
	return mars_data
