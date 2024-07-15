# Importing essential libraries

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
from flask import Flask, render_template, request
import re
from datetime import datetime
from pymongo import MongoClient


class WebScraper:

    def __init__(self,url):
        self.url = url
        self.rpm = []
        self.link = []

        
    # Using BeautifulSoup to collect and storing raw data from webpage
    def scrape_data(self):
        with urlopen(self.url) as response:
            soup =BeautifulSoup(response, 'html.parser')

            texts = soup.find_all('pre')
            for text in texts:
                lines = text.get_text().split('\n')
                for line in lines[2:]:
                    if line.strip():
                        self.rpm.append(line.strip())

            for anchor in soup.find_all('a')[2:]:
                self.link.append(anchor.get('href','/'))

            
    # Data wrangling
    def dataframe(self):
        name = []
        version = []
        gitID = []
        timestamp=[]
        epoch_timestamp = []
        size = []

        for i in self.rpm:
            temp = i.split()    
            timestamp.append(temp[1] + ' ' + temp[2])
            size.append(temp[3])

        for i in timestamp:
            time = datetime.strptime(i ,'%d-%b-%Y %H:%M')
            epoch_timestamp.append(time.timestamp())

        for i in self.link:
            name.append(i[:i.index("-1")])

            version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', i)
            temp = version_match.group(1) if version_match else None
            version.append(temp)
        
            gitID.append(i[i.index(".1.") + 3 : i.find(".el8") or i.index(".noarch")])


            df = pd.DataFrame(list(zip(name, version, gitID,epoch_timestamp, size)), columns=['Name', 'Version', 'GitID','Timestamp','Size'])
        
        return df

    # Pushing Data into MongoDB
    def push_df(self,df):
        client = MongoClient("mongodb://192.168.204.129:27017")
        db = client["Project"]
        

        data = df.to_dict(orient='records')
        # Handling Duplicates by update() 

        for i in data:
            result = db.rpm.update_many({'Name': i['Name']}, {'$set': i}, upsert=True)


app = Flask(__name__)

# Establish a connection to MongoDB
client = MongoClient("mongodb://192.168.204.129:27017/")    
db = client["Project"]
collection = db["rpm"]



# Function to query MongoDB and return results
def query_mongodb(query):                             
    # using regex to search substring in name
    regex_query = re.compile(re.escape(query), re.IGNORECASE)
    results = collection.find({"Name": {'$regex': regex_query}})
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form["name"]
        results = query_mongodb(user_name)
        return render_template("index.html", results=results)

    return render_template("index.html", results=None)
        



if __name__ == "__main__":
    url = "https://nw-fs.tier2.reston.netwitness.com/YUM/alma8/NW/12.4/12.4.0/12.4.0.0-dev/"
    scraper = WebScraper(url)
    rawData = scraper.scrape_data()
    frame = scraper.dataframe()
    temp = scraper.push_df(frame)
    app.run(debug=True)
