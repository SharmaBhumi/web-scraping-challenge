from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_dict")

@app.route('/')
def home():
    mars_news = mongo.db.collection.find_one()
    return render_template('index.html', Mars_dict=mars_news)


@app.route('/scrape')
def scrape():
    mars_data=mongo.db.mars_data
    Mars_dict = scrape_mars.scrape_mars()
    mars_data.update({}, Mars_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
