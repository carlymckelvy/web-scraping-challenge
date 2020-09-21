#Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path":"C:\\Users\\carly\\Documents\\bootcamp\\Chrome_Driver\\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #pause
    time.sleep(1)

    #latest news
    results = soup.find('div', class_="list_text")

    #news title
    results2 = results.find('div', class_="content_title").text

    #news text
    results3 = results.find('div', class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    time.sleep(1)
    browser.find_by_id('full_image').click()

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(1)
    featured_image_url = soup.find("img", class_= "fancybox-image").get("src")
    featured_image_url


    #Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, 
    #Mass, etc.

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    table = pd.read_html(url)[0]

    html_table = table.to_html()

    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all("div", class_= "description")
    hemisphere_image_urls = []

    for item in items:
        title = item.find("h3")
        title_text = title.text.replace("Enhanced", "")
        href = item.find("a").get("href")
        link = ("https://astrogeology.usgs.gov" + href)
        browser.visit(link) 
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        image = soup.find("div", class_ = "content")
        img_url = image.find("a").get("href")
        
        hemisphere_image_urls.append({"title": title_text, "image_url": img_url})
        
        browser.visit(url)

    mars_data = {
        "news_title": results2,
        "news_text": results3,
        "featured_image": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_images": hemisphere_image_urls,
    }

    browser.quit()

    return mars_data



