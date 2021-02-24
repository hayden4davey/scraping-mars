# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of flask
app = Flask(__name__)

# Establish mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Renders index.html template using data from mongo
@app.route("/")
def index():
    
    # Find data from mongo
    mars_data = mongo.db.collection.find_one()
    
    # Return data in template
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape_mars
@app.route("/scrape")
def scrape():

    # Run scrape
    mars_data = scrape_mars.scrape()
    
    # Update mongodb
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)