import plotly
import plotly.graph_objects as go
import pymongo
import pandas as pd

# Import all my functions from geo.py
from geo import get_country_border
from geo import get_bbox
from geo import draw_bbox
from geo import get_country_geojson
from geo import get_within_box

# for sorting 
def getKey(item):
    return item[1]

# using pymongo to interface with my mongo database image (mongodb) in docker
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
"""uf = db["ufos"]
me = db["meteorites"]
vo = db["volcanos"]"""
co = db["countries"]

#events = ["ufos", "meteorites", "volcanos"]

cursor_countries = co.distinct("properties.ADMIN")
df = pd.DataFrame(list(cursor_countries))

# dictionary of countries
country_instances = {}

# temporary list to find top 5 countries with the most of each event
country_instances_temp = []

# for event in events: # run through the three cataclysms
for obj in df[0]: # run through each country in world    
    country_border = get_country_border(obj) # get dictionary of country border points
    country_bbox = get_bbox(country_border) # get dictionary of country bounding box points
    country_box_lats, country_box_lons = draw_bbox(country_bbox) # returns lists of country border lats and lons
    events_in_country = get_within_box("ufos",country_bbox) # return list of events inside country
    
    country_instances_temp.append((obj, len(events_in_country)))

    # save the event and country bbox data in the dictionary
    #if obj not in country_instances:
    country_instances[obj] = [events_in_country, country_box_lats, country_box_lons]

# sorts list of tuples by second value (number of events)
country_instances_temp = sorted(country_instances_temp, key=getKey, reverse=1)

figure = go.Figure()
country_event_lats = []
country_event_lons = []

# loop through the top 5 most event-stricken countries and plot them on plotly
for x in range(0, 6):
    country = country_instances_temp[x][0]
    events_in_country, country_box_lats, country_box_lons = country_instances[country]
    for event in events_in_country:
        country_event_lats.append(event["latitude"])
        country_event_lons.append(event["longitude"])
    figure.add_trace(go.Scattermapbox(
                        lon = country_event_lons,
                        lat = country_event_lats,
                        mode = 'markers',
                        name = country,
                        marker = go.scattermapbox.Marker(size = 3)
    ))
    country_event_lats = []
    country_event_lons = []
figure.update_layout(
    autosize = True,
    template="plotly_dark",
    hovermode="closest",
    mapbox = go.layout.Mapbox(  accesstoken="pk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uMGhsMzAwMGszaW11OXZhempxMTMifQ.tQp7BareQGxwalQvIQvBsw",
                                bearing = 0,
                                center = go.layout.mapbox.Center(lat = 33.9137, lon = -98.4934),
                                pitch = 0,
                                zoom = 5),
    title="Top 5 most eventful countries in the world")

figure.show()