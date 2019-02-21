from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
import pandas as pd

app = Flask(__name__)

# Create connection to MongoDB database `weather_db` and collection `forecasts`
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mission

# Create route that renders index.html template and finds documents from mongo
@app.route('/')
def index():
    mission = collection.find_one()
    return render_template('index.html', mission=mission)

# Create route that will trigger scrape functions
@app.route('/scrape')
def scrape():
    mission = scrape_mars.scrape()
    db.mission.drop()

    # Insert forecast into database
    collection.insert_one(mission)

    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)