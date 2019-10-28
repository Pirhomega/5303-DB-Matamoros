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
co = db["countries"]
cursor_countries = co.distinct("properties.ADMIN")
df = pd.DataFrame(list(cursor_countries))

# some initializations
events = [("ufos", go.Figure()), ("meteorites", go.Figure()), ("volcanos", go.Figure())]
country_event_lats = []
country_event_lons = []
country_colors = ['red', 'yellow', 'blue', 'green', 'white']

# dictionary of countries
country_instances = {}

# temporary list to find top 5 countries with the most of each event
country_instances_temp = []

# run through the three cataclysms
for cataclysm in events: 
    for obj in df[0]: # run through each country in world    
        country_border = get_country_border(obj) # get dictionary of country border points
        country_bbox = get_bbox(country_border) # get dictionary of country bounding box points
        country_box_lats, country_box_lons = draw_bbox(country_bbox) # returns lists of country border lats and lons
        events_in_country = get_within_box(cataclysm[0],country_bbox) # return list of events inside country
        
        country_instances_temp.append((obj, len(events_in_country)))

        # save the event and country bbox data in the dictionary
        country_instances[obj] = [events_in_country, country_box_lats, country_box_lons]

    # sorts list of tuples by second value (number of events)
    country_instances_temp = sorted(country_instances_temp, key=getKey, reverse=1)

    figure = cataclysm[1]

    # loop through the top 5 most event-stricken countries and plot them on plotly
    for x in range(0, 5):
        country = country_instances_temp[x][0]
        events_in_country, country_box_lats, country_box_lons = country_instances[country]
        for event in events_in_country:
            country_event_lats.append(event["latitude"])
            country_event_lons.append(event["longitude"])
        
        # configure the imaging with plotly to display events in country
        figure.add_trace(go.Scattermapbox(
                            lon = country_event_lons,
                            lat = country_event_lats,
                            mode = 'markers',
                            name = country,
                            marker = go.scattermapbox.Marker(size = 3)
        ))

        # configure the imaging with plotly to display country borders
        figure.add_trace(go.Scattermapbox(
                        lon = country_box_lons,
                        lat = country_box_lats,
                        mode = 'lines',
                        name = country,
                        line = dict(width = 2, color = country_colors[x])
        ))

        # empty lists so I can append new data on without muddling the old data
        country_event_lats = []
        country_event_lons = []

    # sets the layout for plotting
    figure.update_layout(
        autosize = True,
        template="plotly_dark",
        hovermode="closest",
        mapbox = go.layout.Mapbox(  accesstoken="pk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uMGhsMzAwMGszaW11OXZhempxMTMifQ.tQp7BareQGxwalQvIQvBsw",
                                    bearing = 0,
                                    center = go.layout.mapbox.Center(lat = 33.9137, lon = -98.4934),
                                    pitch = 0,
                                    zoom = 5),
        title="Top 5 most " + cataclysm[0] + "-stricken countries in the world")

    figure.show(renderer='iframe')