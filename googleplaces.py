API_KEY = 'AIzaSyC7XL6xx5ADHM_1recyCG8zUZ9OT3mbKj4'
import urllib
import sqlite3
import requests
import json
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
key_string = '&key=' + API_KEY                                
conn = sqlite3.connect('fulldata.sqlite')
cur = conn.cursor()
places = list(cur.execute('SELECT name, city FROM yelp_ratings'))
jsons = []
coordinates = [(41.89235,-87.66198), (40.7128, -74.0060), (47.6062,-122.3321), (36.1627,-86.7816), (42.3601,-71.0589)]
googlerestaurants = []
for c in coordinates:
    lat = c[0]
    lng = c[1]
    location = str(lat) + ',' + str(lng)
    MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        '?location=%s'
        '&rankBy=distance&radius=%s'
        '&name=%s'
        '&key=%s') % (location, 200000, 'restaurant', 'AIzaSyC7XL6xx5ADHM_1recyCG8zUZ9OT3mbKj4')
    response = urllib.request.urlopen(MyUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    googlerestaurants.append(jsonData)


#print(googlerestaurants)


restaurant_info = []
for x in googlerestaurants: 
    rest = x["results"]
    for r in rest: 
        current_restaurant = {}
        current_restaurant['name'] = r['name']
        current_restaurant['rating'] = r['rating']
        if 'price_level' in r:
            current_restaurant['price'] = r['price_level']
        else: 
            current_restaurant['price'] = None 
        current_restaurant['city'] = r['plus_code']['compound_code']
        restaurant_info.append(current_restaurant)



conn = sqlite3.connect('fulldata.sqlite')
cur = conn.cursor()
#cur.execute("DROP TABLE IF EXISTS google_ratings")
cur.execute('CREATE TABLE IF NOT EXISTS google_ratings (name TEXT, rating INTEGER, price INTEGER, city TEXT)')
for x in restaurant_info: 
    restaurantname = x['name']
    cur.execute('SELECT Name FROM google_ratings WHERE Name = ? LIMIT 1', (restaurantname,))
    try:
        hi = cur.fetchone()[0]
    except: 
        cur.execute('INSERT INTO google_ratings (name, rating, price, city) VALUES (?, ?, ?, ?)', (x['name'], x['rating'], x['price'], x['city']))
    conn.commit()


