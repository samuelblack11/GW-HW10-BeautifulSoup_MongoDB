from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
# this pulls in the scrape_craigslist.py file
import scrape_mars

app = Flask(__name__)



# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_stuff = mongo.db.collection.find_one()

    return render_template("index.html", mars_dict=mars_stuff)

@app.route("/hemispheres.html")
def hemispheres():
    mars_stuff = mongo.db.collection.find_one()

    return render_template("hemispheres.html", mars_dict=mars_stuff)



@app.route("/scrape")
def scraper():
	#conn = 'mongodb://localhost:27017'
	#client = pymongo.MongoClient(conn)
	## Define the 'classDB' database in Mongo
	#db = client.classDB
	#mars_db=db.mars_db
	#result = mars_db.insert_one(facts_images_dict)
    
	mars_dict=scrape_mars.scrape()
	#mars_dict=mongo.db.mars_dict
	mongo.db.collection.update({}, mars_dict, upsert=True)
	return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)


