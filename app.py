#imports
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#use flask pymongo to set up connection to database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    #access information from database
    mars_data = mongo.db.mars_data.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #reference to database collection
    marsTable = mongo.db.mars_data

    #drop table if it exists
    mongo.db.mars_data.drop()

    #call scrape mars script
    mars_data = scrape_mars.scrape_all()

    #take dictionary and load it into mongo db
    marsTable.insert_one(mars_data)

    #go back to index route
    return redirect("/")

if __name__ == "__main__":
    app.run()