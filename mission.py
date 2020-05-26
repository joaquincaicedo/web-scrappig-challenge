#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import datetime as time


# In[2]:


#Headline URL
headline_url = "https://mars.nasa.gov/news/"
#Image URL
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#Twitter URL
twitter_url = "https://twitter.com/marswxreport?lang=en"
#Facts URL
facts_url = "https://space-facts.com/mars/"
#Hemispheres URL
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"



def news(headline_url):
    try:
        browser = Browser('chrome', executable_path=r"C:\webdrivers\chromedriver.exe")
        browser.visit(headline_url)
        content = browser.html
        browser.is_element_present_by_css("ul.item_list li.slide" , wait_time = 1)
        news = BeautifulSoup(content, "html.parser")
        element = news.select_one("ul.item_list li.slide")
        element.find("div", class_="content_title")
        news_title = element.find("div", class_="content_title").get_text()
        news_p = element.find("div", class_="article_teaser_body").get_text()
    except:
        return 
    return news_title, news_p


def images(image_url):
    try:
        browser = Browser('chrome', executable_path=r"C:\webdrivers\chromedriver.exe")
        browser.visit(image_url)
        full_size = browser.find_by_id("full_image")
        full_size.click()
        browser.is_element_present_by_text("more info", wait_time=1)
        more_info = browser.links.find_by_partial_text("more info")
        more_info.click()
        content = browser.html
        image_soup = BeautifulSoup(content, "html.parser")
        image = image_soup.select_one("figure.lede a img")
        image_url = image.get("src")
    except AttributeError:
        return 
    featured_image_url  = f"https://www.jpl.nasa.gov{image_url}"
    return featured_image_url

def twitter(twitter_url):
    try:
        browser = Browser('chrome', executable_path=r"C:\webdrivers\chromedriver.exe")
        browser.visit(twitter_url)
        content =  browser.html
        weather = BeautifulSoup(content, "html.parser")
        weather_tweet = weather.find("div", params = {
                                               "class": "tweet", 
                                                "data-name": "Mars Weather"
                                                })
        mars_weather = weather_tweet.find("p", "tweet-text").get_text()
    except AttributeError:
        return 
    return mars_weather     

def facts(facts_url):
    try:
        df = pd.read_html(facts_url)[0]
    except AttributeError:
        return 
    df.columns=["Profile", "Value"]
    df.set_index("Profile", inplace=True)
    return df

def hemisphere(hemispheres_url):
    try:
        browser = Browser('chrome', executable_path=r"C:\webdrivers\chromedriver.exe")
        browser.visit(hemispheres_url)
        hemisphere_urls = []
        item_count = browser.find_by_css("a.product-item h3")
        for i in range(len(item_count)):
            hemisphere = {}
            browser.find_by_css("a.product-item h3")[i].click()
            hemisphere["name"] = browser.find_by_css("h2.title").text
            image = browser.links.find_by_text("Sample").first
            hemisphere['image_url'] = image['href']
            hemisphere_urls.append(hemisphere)
            browser.back()
    except AttributeError:
        return 
    return hemisphere_urls
            

def scrape():
    try:
        browser = Browser('chrome', executable_path=r"C:\webdrivers\chromedriver.exe")
        news_title, news_p = news(headline_url)
        img_url = images(image_url)
        mars_weather = twitter(twitter_url)
        facts_df = facts(facts_url)
        facts_html = facts.to_html(classes="table table-striped")
        hemisphere_image_urls = hemisphere(hemispheres_url)
        timestamp = time.datetime.now()

        data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": img_url,
            "weather": mars_weather,
            "facts": facts,
            "hemispheres": hemisphere_image_urls,
            "last_modified": timestamp
        }
        browser.quit()
    except:
        return
    return data 

if __name__ == "__main__":
    print(scrape())
        
        





