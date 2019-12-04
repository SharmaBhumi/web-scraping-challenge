# Web Scraping - Mission to Mars

![mission_to_mars](Images/mission_to_mars.png)

In this web application data is scraped from various websites for data related to the Mission to Mars and the information in a single is displayed on an HTML page. The following outlines what is done.

## Step 1 - Scraping

Initial scraping is done using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

* Created a Jupyter Notebook file called `mission_to_mars.ipynb` and used it to complete all the scraping and analysis tasks. The following outlines what is scraped.

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text.

### JPL Mars Space Images - Featured Image

* url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Used splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

### Mars Weather

* Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en).Scrape the latest Mars weather tweet from the page. Saved the tweet text for the weather report as a variable called `mars_weather`.

### Mars Facts

* Mars Facts webpage [here](https://space-facts.com/mars/)
* Used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. and to convert the data to a HTML table string.

### Mars Hemispheres

* USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

* Saved both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Used a Python dictionary to store the data using the keys `img_url` and `title`.

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* First converted the Jupyter notebook into a Python script called `scrape_mars.py` with a function called `mars_scrape` that will execute all of the scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, created a route called `/scrape` that will import the `scrape_mars.py` script and call the `scrape` function.

  * Stored the return value in Mongo as a Python dictionary.

* Created a root route `/` that will query the Mongo database and pass the mars data into an HTML template to display the data.

* Created a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements.
