from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_ = 'list_text')
    news_title = article.find("div", class_ = "content_title").text
    news_p = article.find("div", class_ = "article_teaser_body").text
    news_info = [news_title, news_p]
    return news_info

def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts

def marsHem():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemispheres = soup.find_all('div', class_ = 'item')
    hemisphere_image_urls = []
    
    for x in hemispheres:
        title = x.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = x.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_ = "downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title" : title, "img_url" : image_url})
    return hemisphere_image_urls


def scrape():
    first_article = marsNews()
    title = first_article[0]
    paragraph = first_article[1]
    featured_image = marsImage()
    facts = marsFacts()
    hemispheres = marsHem()

    compressed_scrape = {'news_title' : title,
                        'news_paragraph' : paragraph,
                        'featured_img' : featured_image,
                        'facts' : facts,
                        'hemispheres' : hemispheres}
    return compressed_scrape