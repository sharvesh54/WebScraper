# Web Scraper with Flask and MongoDB

## Overview

This Python-based web scraper is designed to collect data from a specified webpage, perform data wrangling, and store the cleaned data in a MongoDB database. It leverages popular libraries such as BeautifulSoup for web scraping, Flask for creating a simple web interface to query the collected data, and pymongo for interacting with MongoDB.

## Prerequisites

Before using this code, ensure that you have the following prerequisites installed:

- *Python 3.x:* This code is written in Python, so you'll need a Python interpreter to run it.

- *Flask:* Flask is a lightweight web framework for Python. It's used in this project to create a web interface.

- *BeautifulSoup:* BeautifulSoup is a Python library for parsing HTML and XML documents. It's employed for web scraping.

- *pandas:* The pandas library provides data structures for efficient data manipulation and analysis. It's used for data wrangling.

- *pymongo:* pymongo is a Python driver for MongoDB. You'll need this to interact with your MongoDB database.

- *MongoDB:* You should have access to a MongoDB server or have MongoDB installed locally. Make sure to configure the MongoDB connection appropriately.

## Installation

1. *Clone the Repository:*

   ```shell
   git clone https://github.com/sharvesh54/WebScraper.git
   cd your-repo
   ```
  
2. *Install Dependencies:*
      
      ```
      pip install flask beautifulsoup4 pandas pymongo
      ```
      
3. *Configure MongoDB connection:*
        
     In the **WebScraper** class and the flask app section of the code, replace  
     ```
     client = MongoClient("mongodb://192.168.204.129:27017")
     ```
     with the connection string for your MongoDB server.

