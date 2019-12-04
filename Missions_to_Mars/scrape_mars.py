#!/usr/bin/env python
# coding: utf-8


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd

def scrape_mars():

#Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract title text
    title = soup.title.text
    print(title)

    # Print all paragraph texts
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        news_p=paragraph.text
        print(news_p)

#Featured Image for Mars
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    articles = soup.find_all('article', class_='carousel_item')
    for article in articles:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            f = article.find('footer')
            link = f.find('a')
            href = link['data-fancybox-href']
            featured_image_url ='https://www.jpl.nasa.gov'+ href
    #         title = link['data_title']
            print('-----------')
            print(title)
            print(link.text.strip())
            print(featured_image_url)

    browser.quit()

#twitter data for latest Mars weather data
    twitter_browser = Browser('chrome', **executable_path, headless=False)
    tweet_url='https://twitter.com/marswxreport?lang=en'
    twitter_browser.visit(tweet_url)

    # Retrieve page with the requests module
    twitter_html = twitter_browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    tweet_soup = BeautifulSoup(twitter_html, 'lxml')
    # Extract title text
    tweet_title = tweet_soup.title.text
    print(tweet_title)

    results=tweet_soup.find_all('div',class_='js-tweet-text-container')

    tweet=results[0].prettify().split('\n')
    # print(tweet)
    mars_weather=tweet[2].strip()+" "+tweet[3]+" "+tweet[4]
    print(mars_weather)
    twitter_browser.quit()


    #Mars Facts
    browser = Browser('chrome', **executable_path, headless=False)
    mars_fact_url='https://space-facts.com/mars/'
    browser.visit(mars_fact_url)
    space_html = browser.html
    space_soup = BeautifulSoup(space_html, 'lxml')
    space_table = space_soup.find('table', class_="tablepress tablepress-id-p-mars")

    mars_df = pd.read_html(mars_fact_url)[0]
    mars_df.columns=['profile','facts']
    mars_df.set_index('profile', inplace=True)
    mars_df

    html_table = mars_df.to_html()
    html_table.replace('\n', '')
    html_table

    browser.quit()

#Mars Hemisphere images
    executable_path = {'executable_path': 'chromedriver.exe'}
    USGS_browser = Browser('chrome', **executable_path, headless=False)
    USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    USGS_browser.visit(USGS_url)


    USGS_html = USGS_browser.html
    USGS_soup = BeautifulSoup(USGS_html, 'lxml')

    hemisphere_image_urls = []
    USGS_hemis_a = USGS_soup.find_all('div', class_="item")
    main_url = "https://astrogeology.usgs.gov"
    for hemi in USGS_hemis_a:
        USGS_title = hemi.h3.text[:-9]
        USGS_hemi_url = main_url+hemi.a['href']
        USGS_browser.visit(USGS_hemi_url)
        USGS_img_html = USGS_browser.html
        USGS_img_soup = BeautifulSoup(USGS_img_html, 'html.parser')
        #print(USGS_img_soup)
        part_url = USGS_img_soup.find('img', class_='wide-image')['src']
        USGS_img_url = main_url + part_url
        hemi_dict = {"title":USGS_title,"img_url": USGS_img_url}
        hemisphere_image_urls.append(hemi_dict)
    hemisphere_image_urls

    USGS_browser.quit()

#Dictionary for the collected Mars data
    Mars_dict = {"Heading": title,
                "Summary": news_p, 
                "Featured_Image": featured_image_url,
                "Mars_Weather": mars_weather,
                "Mars_Facts": html_table,
                "Mars_hemisphere": hemisphere_image_urls}


    print(Mars_dict)
    return Mars_dict




