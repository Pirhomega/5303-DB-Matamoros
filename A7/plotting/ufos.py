import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
ufos = db["ufos"]

# iterate through mongodb collection and create a pandas dataframe with the collection data
cursor_ufos = db.ufos.find()
df = pd.DataFrame(list(cursor_ufos))

# sets the geospatial data up
data = go.Figure([go.Scattermapbox( lat = df["latitude"], 
                                    lon = df["longitude"],
                                    text = df["city"],
                                    mode = 'markers',   
                                    marker=dict(size=4,color='blue',opacity=.8)
                                    ),
                                ])

data.update_layout(
    hovermode='closest',
    mapbox = go.layout.Mapbox(  accesstoken="sk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uNm10czAyaXUzbXJ5aWdtcWF0czQifQ.UFhkWIiTARUXtsAb3nCYpg",
                                bearing = 0,
                                center = dict(lat = 51.47781, lon = 0.0),
                                pitch = 0,
                                zoom = 5))

# sets the layout for plotting
# layout = go.Layout( autosize = False,
#                     mapbox = dict(  accesstoken="sk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uNm10czAyaXUzbXJ5aWdtcWF0czQifQ.UFhkWIiTARUXtsAb3nCYpg",
#                                     bearing = 10,
#                                     pitch = 60,
#                                     zoom = 13,
#                                     center = dict(lat = 51.47781, lon = 0.0)),
#                     width = 900,
#                     height = 600,
#                     title = "UFO Sightings Test 1.0")

# plot the data
# fig = dict(data = data, layout = layout)
data.show()