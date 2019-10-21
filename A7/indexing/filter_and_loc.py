#!/usr/local/bin/python3
"""
This file cleans the airport collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
cities = db["cities"]

count = 0

# loop through every document, check if the lat and lons are numbers
# If they are, update document with new field
# If they aren't, remove document entirely
for obj in cities.find():
    mongo_id = obj["_id"]
    lat = obj["lat"]
    lon = obj["lng"]
    # Check if lat and lon are ints or floats
    lati = isinstance(lat, int)
    loni = isinstance(lon, int) 
    flat = isinstance(lat, float)
    flon = isinstance(lon, float)

    # use the two variables below to check if the lat and lon values are strings
    # latf = isinstance(lat, str)
    # lonf = isinstance(lon, str)
    
    # run the if statement below of your lat and lon data are stored as strings
    """if (latf or lonf):
        # flat = float(lat)
        # flon = float(lon)
        cities.update_one({'_id':mongo_id}, {'$set': {'lat': float(lat)}}, upsert=False)
        cities.update_one({'_id':mongo_id}, {'$set': {'lng': float(lon)}}, upsert=False)"""
        
    # If the lat lons ARE numbers, insert it
    if (lati or flat) and (loni or flon):
        cities.update_one({'_id':mongo_id}, {"$set": {"loc" : { "type": "Point", "coordinates": [ lon, lat ] }}}, upsert=False)
    else:
        print(f"Removing: {lat},{lon}")
        cities.delete_one({'_id':mongo_id})
        count += 1
        
print(f"Count not inserted: {count}")
