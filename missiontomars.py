#!/usr/bin/env python
# coding: utf-8

# In[7]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template


# In[ ]:


#NASA Mars News
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# Example:
#news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
#news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."


# In[2]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[35]:



url ='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)
# Retrieve page with the requests module
#response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = bs(browser.html, "html.parser")
result = soup.findAll("div", class_="content_title")
title = result[1].a.text


# In[36]:


mars = {}


# In[37]:


soup.find_all('a')


# In[38]:


mydivs = soup.findAll("div", {"class": "article_teaser_body"})
paragraph = mydivs[0].text
paragraph


# In[ ]:


mars["news_title"] = title
mars["news_p"]= paragraph


# In[ ]:


#PL Mars Space Images - Featured Image
#Visit the url for JPL Featured Space Image here.
#Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
#Make sure to find the image url to the full size .jpg image.
#Make sure to save a complete url string for this image.
# Example:
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'


# In[11]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
fullimage = browser.find_by_id("full_image").click()
findlink = browser.find_link_by_partial_text("more info").click()


# In[18]:


soup = bs(browser.html, "html.parser")
fimage = soup.find("figure", class_ = "lede")
fullimage = fimage.a.img["src"]
final_image_link = "https://www.jpl.nasa.com"+fullimage
final_image_link


# In[29]:


mars["featured_image_url"] = final_image_link


# In[ ]:


#Mars Weather
#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
#Note: Be sure you are not signed in to twitter, or scraping may become more difficult.
# Example:
#mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'


# In[54]:



url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)  
soup = bs(browser.html, "html.parser")
tweet = soup.findAll("span", class_="css-1dbjc4n r-13awgt0 r-12vffkv")

                     


# In[ ]:


mars_weather


# In[ ]:


#Mars Facts
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#Use Pandas to convert the data to a HTML table string.


# In[20]:


url1= 'https://space-facts.com/mars/'


# In[30]:


# Use Panda's `read_html` to parse the url
### BEGIN SOLUTION
tables = pd.read_html(url1)
tables
### END SOLUTION
table_html = tables[0].to_html()
mars["facts"] = table_html


# In[ ]:


#Mars Hemispheres
#Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
#You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
#Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
#Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]


# In[ ]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
soup = bs(browser.html, "html.parser")
tweet = soup.findAll("span", class_="css-1dbjc4n r-13awgt0 r-12vffkv")


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    marsmission_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mmission=marsmission_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)