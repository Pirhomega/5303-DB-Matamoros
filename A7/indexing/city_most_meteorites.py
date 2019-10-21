import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
meteorites = db["meteorites"]
cities = db["cities"]

