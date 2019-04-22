from yelpapi import YelpAPI
import requests
import sqlite3

restaurant_info = []
cities = ["Chicago", "New York", "Seattle", "Nashville", "Boston"]

for city in cities: 
 
        yelp_api = YelpAPI("rUEC-ExRMZtk-gtHzjLDVJ1X07Rubbxe_s13I4gop_auCUueHmmy57u132SChk6fLvstzqYkLymaijUc7VPGnh9yVaERdkXXX34qsHv80YcvFfEcWlHz0j4kpQmtXHYx")
        search_results = yelp_api.search_query(term = "restaurants", location = city , sort_by = "rating", limit = 20)
        for x in search_results['businesses']: 
                current_restaurant = {}
                current_restaurant["name"] = x['name']
                current_restaurant["category"] = (x['categories'][0]['title'])
                current_restaurant["latitude"] = x['coordinates']['latitude']
                current_restaurant["longitude"] = x['coordinates']['longitude']
                current_restaurant["rating"] = x["rating"]
                current_restaurant["city"] = city
                if 'price' in x:
                        current_restaurant["price"] = x["price"]
                else:
                        current_restaurant["price"] = None
                restaurant_info.append(current_restaurant)
        
        conn = sqlite3.connect('fulldata.sqlite')
        cur = conn.cursor()
        #cur.execute("DROP TABLE IF EXISTS yelp_ratings")
        cur.execute('CREATE TABLE IF NOT EXISTS yelp_ratings (City TEXT, Name TEXT, Category TEXT, Latitude INTEGER, Longitude INTEGER, Rating INTEGER, Price TEXT)')
        for x in restaurant_info:
                restaurantname = x['name']
                cur.execute('SELECT Name FROM yelp_ratings WHERE Name = ? LIMIT 1', (restaurantname,))
                try:
                        hi = cur.fetchone()[0]
                except:
                        cur.execute('INSERT INTO yelp_ratings (City, Name, Category, Latitude, Longitude, Rating, Price) VALUES (?,?,?,?,?,?,?)', (x['city'], x['name'], x['category'], x['latitude'], x['longitude'], x['rating'], x['price']))
                conn.commit()


  


