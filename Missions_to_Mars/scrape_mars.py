import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup


def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slides = soup.find_all('li', class_='slide')
    content_title = slides[0].find('div', class_ = 'content_title')
    news_title = content_title.text.strip()
    article_teaser_body = slides[0].find('div', class_ = 'article_teaser_body')
    news_p = article_teaser_body.text.strip()

    # JPL Mars Space Images - Featured Image
    base_url = "https://www.jpl.nasa.gov"
    url = base_url + "/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find("a", class_ = "button fancybox")["data-fancybox-href"]
    featured_image_url = base_url + href

    # Mars Facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    table_df = tables[0]
    table_df.columns = ['Fact', 'Value']
    table_df["Fact"]= table_df["Fact"].str.replace(":","")
    table_html = table_df.to_html()

    # Mars Hemispheres
    base_url = "https://astrogeology.usgs.gov/"
    url = base_url + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_ = "item")
    titles = []
    urls = []
    for item in items:
        titles.append(item.find("h3").text.strip())
        urls.append(base_url + item.find("a")["href"])
    img_url = []
    for url in urls:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find("div",class_='downloads')
        img_url.append(item.find_all("li")[1].find("a")["href"])
    hemisphere_image_urls = []
    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_url[i]})


    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["table_html"] = table_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage