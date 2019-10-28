#!/usr/local/bin/python3
"""
This file cleans the airport collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
plane = db["plane_crashes"]

count = 0

# loop through every document, check if the lat and lons are numbers
# If they are, update document with new field
# If they aren't, remove document entirely
for obj in plane.find():
    mongo_id = obj["_id"]
    lat = obj["Latitude"]
    lon = obj["Longitude"]
    fatal = obj["TotalFatalInjuries"]
    
    # If the lat lons ARE numbers, insert it
    if (lat != "  " and lon != "  ") and (lat != None and lon != None):
        print("It's cool")
    else:
        plane.delete_one({'_id':mongo_id})
        count += 1
    if fatal == "  " or fatal == None:
        plane.delete_one({'_id':mongo_id})
        
print(f"Count deleted: {count}")
