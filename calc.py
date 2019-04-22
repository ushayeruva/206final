import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import json
import numpy as np
conn = sqlite3.connect('fulldata.sqlite')
cur = conn.cursor()
restaurant = list(cur.execute('SELECT name, city, rating FROM yelp_ratings'))

f = open("calc.txt", "w")

cities = ["Chicago", "New York", "Seattle", "Nashville", "Boston"]
yelprating = {}
googlerating = {}
yelpcity_ratings = []
cityratingtup = []

for city in cities: 
    cur.execute('SELECT rating FROM yelp_ratings WHERE city = ? LIMIT 100', (city,))
    yelp = cur.fetchall()
    a = 0 
    for y in yelp:
        a += y[0]
    avgrating = a / len(yelp)
    yelprating[city] = avgrating

#print (yelprating)
cur.execute('SELECT rating , city FROM google_ratings')
messy = cur.fetchall()
IL = []
NY = []

googleratingFIRST = {}
for mess in messy:
    state = mess[1]
    state = state[8:]
    state = state[:-5]
    state = state.replace(" ", "")
    state = state.split(',')
    if len(state) == 3:
        state = state[2]
    elif len(state) == 2:
        state = state[1]
    elif len(state) == 1:
        state = state[0]
        
    if state == "IL":
        state = "Chicago"
    elif state == "Illinois":
        state = "Chicago"
    elif state == "TN":
        state = "Nashville"
    elif state == "Tennessee":
        state = "Nashville"
    elif state == "Washington":
        state = "Seattle"
    elif state == "NewYork":
        state = "New York"
    elif state == "NY":
        state = "New York"
    elif state == "NewJersey":
        state = "New York"
    elif state == "Massachusetts":
        state = "Boston"
    elif state == "MA":
        state = "Boston"
    else:
        print("FAILURE")


    if state not in googleratingFIRST:
        googleratingFIRST[state] = [mess[0]]
    else:
        googleratingFIRST[state] += [mess[0]]

a = 0
count = 0
googlerating = {}
for g in googleratingFIRST:
    #print(g)
    for num in googleratingFIRST[g]:
        count += 1
        a += num
    averagerating = a / count
    googlerating[g] = averagerating
#print(googlerating)

f.write("Yelp users' average ratings are as follows: " + str(yelprating) +   
        "\n Google Places users' average ratings are as follows: " + str(googlerating))

f.close()

categories = list(cur.execute('SELECT category FROM yelp_ratings'))

things = []
for c in categories: 
    things.append(c[0])

category_types = {}
for cat in things:
    if cat in category_types:
        category_types[cat] += 1 
    else:
        category_types[cat] = 1 
newcategories = {}
newcategories["American"] = category_types['American (New)'] + category_types["Pizza"] + category_types['American (Traditional)'] + category_types['Southern'] + category_types['Burgers'] + category_types['Sandwiches']
newcategories["Ethnic Cuisine"] = category_types['Empanadas'] + category_types['Filipino'] + category_types['Lebanese'] + category_types['Sushi Bars']
+ category_types['Bangladeshi'] + category_types["Dominican"] + category_types["Thai"]
newcategories["Sushi"] = category_types['Sushi Bars'] + category_types['Poke'] + category_types['Seafood']
newcategories["Italian"] = category_types["Italian"]
newcategories["Bakeries"] = category_types["Bakeries"] + category_types['Cafes']
sorted_dict = sorted(category_types, key = lambda x: x[1], reverse = True)

labels = ['American', 'Ethnic Cuisine', 'Sushi', 'Italian', 'Bakeries']
sizes = [newcategories['American'], newcategories["Ethnic Cuisine"], newcategories["Sushi"], newcategories["Italian"], newcategories["Bakeries"]]
plt.title("Distribution of Categories of Restaurants")
plt.pie(sizes, labels = labels, autopct='%1.1f%%', shadow=True, startangle=90, colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"])
plt.savefig("categories.png")
plt.show()

prices = list(cur.execute('SELECT price FROM google_ratings'))
items = []
for price in prices:
    items.append(price[0])
price_dict = {}
for x in items:
    if x not in price_dict:
        price_dict[x] = 1 
    else:
        price_dict[x] += 1 


data = price_dict 
labels = ["1", "2", "3", "4"]
counts = [data[1], data[2], data[3], data[4]]
plt.bar(labels, counts, align = "center", color = ["#E13F29", "#D69A80", "#D63B59", "#AE5552"])
plt.xlabel("Price Range")
plt.ylabel("Number of Restaurants")
plt.title("Restaurants at Different Price Ranges")
plt.savefig("prices.png")
plt.show()


ratings = list(cur.execute('SELECT rating FROM google_ratings'))
items = []
for rating in ratings:
    items.append(rating[0])
google_ratings_dict = {}
for x in items:
    if x not in google_ratings_dict:
        google_ratings_dict[x] = 1
    else:
        google_ratings_dict[x] += 1 




data = google_ratings_dict
labels = ["4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9"]
counts = [data[4.3], data[4.4], data[4.5], data[4.6], data[4.7], data[4.8], data[4.9]]
plt.bar(labels, counts, align = "center", color = ["#96624E", "#EB8076", "#CB5C3B", "#AE5552"])
plt.xlabel("Google Places Ratings")
plt.ylabel("Number of Restaurants")
plt.title("Ratings Distribution")
plt.savefig("ratings.png")
plt.show()





