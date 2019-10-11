#!/usr/local/bin/python3
"""
This file cleans the ufo collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
airports = db["airports"]


count = 0

for obj in airports.find():
    mongo_id = obj["_id"]
    lat = obj["latitude"]
    lon = obj["longitude"]
    # Check if lat and lon are ints or floats
    lati = isinstance(lat, int)
    loni = isinstance(lon, int) 
    flat = isinstance(lat, float)
    flon = isinstance(lon, float)
    
    # If the lat lons ARE numbers, insert it
    if (lati or flat) and (flat or flon):
        airports.update_one({'_id':mongo_id}, {"$set": {"loc" : { "type": "Point", "coordinates": [ lon, lat ] }}}, upsert=False)
    else:
        print(f"Removing: {lat},{lon}")
        airports.remove({'_id':mongo_id})
        count += 1
        
print(f"Count not inserted: {count}")
