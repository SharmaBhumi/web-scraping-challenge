#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd


def scrape_mars():

# NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # Extract title text
    title = soup.title.text
    print(title)
    # Print all paragraph texts
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        news_p=paragraph.text
        print(news_p)


# JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

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
            featured_image_url ='https://www.jpl.nasa.gov/'+ href
    #         title = link['data_title']
            print('-----------')
            print(title)
            print(link.text.strip())
            print(featured_image_url)
    browser.quit()
    


#twitter data for Mars
    tweet_url='https://twitter.com/marswxreport?lang=en'


    # Retrieve page with the requests module
    response = requests.get(tweet_url)
    # Create BeautifulSoup object; parse with 'lxml'
    tweet_soup = BeautifulSoup(response.text, 'lxml')
    # Extract title text
    tweet_title = tweet_soup.title.text
    print(tweet_title)
    results=tweet_soup.find_all('div',class_='js-tweet-text-container')
    tweet=results[0].prettify().split('\n')
    # print(tweet)
    mars_weather=tweet[2].strip()+" "+tweet[3]+" "+tweet[4]
    print(mars_weather)
    

#Mars Facts

     #Scrape Space Facts Mars page
    # Use Pandas
    space_browser = Browser('chrome', **executable_path, headless=False)
    space_url = "https://space-facts.com/mars/"
    space_browser.visit(space_url)
    space_html = space_browser.html
    space_soup = BeautifulSoup(space_html, 'lxml')
    space_table = space_soup.find('table', class_="tablepress tablepress-id-p-mars")
    mars_df = pd.read_html(space_url)[0]
    mars_df.columns = ['Characteristic', 'Fact']
    mars_df.set_index('Characteristic', inplace=True)
    mars_html = mars_df.to_html()
    space_browser.quit()

    

#usgs Mars images
    usgs_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    results=soup.find_all('div', class_='item')

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            title = result.h3.text[:-9]

            link = result.a['href'].strip()
            img_url='https://astrogeology.usgs.gov'+link

            hemi_dict ={'title':title,'img_url':img_url}
            hemisphere_image_urls.append(hemi_dict)


            # Print results only if title, price, and link are available
            if (link):
                print('-------------')
                print(title)
                print(img_url)
        except AttributeError as e:
            print(e)


    hemisphere_image_urls

    browser.quit()


    ## dictionary with scraped details

    Mars_dict = {"Heading": title, \
               "Summary": news_p, \
               "Featured_Image": featured_image_url, \
               "Mars_Weather": mars_weather, \
               "Mars_Facts": mars_html, \
               "Mars_hemisphere": hemisphere_image_urls}

    print(Mars_dict)
    return Mars_dict


