import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.io as pio
import pymongo

# public token to be used by Mapbox
mapbox_token = ""

# using pymongo to interface with my mongo database image (mongodb) in docker
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]

"""iterate through each of the five mongodb collections and create a pandas dataframe with their collection data"""
########################################################################################

# airports
cursor = db.airports.find()
df1 = pd.DataFrame(list(cursor))

# earthquakes
cursor = db.earthquakes.find()
df2 = pd.DataFrame(list(cursor))

# meteorites
cursor = db.meteorites.find()
df3 = pd.DataFrame(list(cursor))

# ufos
cursor = db.ufos.find()
df4 = pd.DataFrame(list(cursor))

# volcanos
cursor = db.volcanos.find()
df5_pre = pd.DataFrame(list(cursor))
df5 = pd.DataFrame(list(df5_pre["properties"]))

########################################################################################

figure = go.Figure()

"""add a different trace/layer to the map formed with each set of data gathered above"""
########################################################################################

# airports
figure.add_trace(go.Scattermapbox(  lat = df1["latitude"], 
                                    lon = df1["longitude"],
                                    text = df1["airport"],
                                    mode = "markers",   
                                    marker=dict(size=8,opacity=.8,symbol="airport")))

# earthquakes
figure.add_trace(go.Scattermapbox(  lat = df2["latitude"], 
                                    lon = df2["longitude"],
                                    text = df2["place"],
                                    mode = "markers",   
                                    marker=dict(size=8,opacity=.8,symbol="danger")))

# meteorites
figure.add_trace(go.Scattermapbox(  lat = df3["reclat"], 
                                    lon = df3["reclong"],
                                    text = df3["name"],
                                    mode = "markers",   
                                    marker=dict(size=8,opacity=.8,symbol="cross")))

# ufos
figure.add_trace(go.Scattermapbox(  lat = df4["latitude"], 
                                    lon = df4["longitude"],
                                    text = df4["city"],
                                    mode = "markers",   
                                    marker=dict(size=8,opacity=.8,symbol="viewpoint")))

# volcanos
figure.add_trace(go.Scattermapbox(  lat = df5["Latitude"], 
                                    lon = df5["Longitude"],
                                    text = df5["V_Name"],
                                    mode = "markers",   
                                    marker=dict(size=8,opacity=.8,symbol="volcano")))

########################################################################################

# Format the figure parameters such as title, size, etc.
figure.update_layout(
    title = "Armageddon - A Visualization of Hell on Earth",
    autosize = True,
    hovermode = 'closest',
    template = "plotly_dark",
    mapbox = go.layout.Mapbox(  accesstoken=mapbox_token,
                                bearing = 0,
                                center = go.layout.mapbox.Center(lat = 33.9137, lon = -98.4934),
                                pitch = 0,
                                zoom = 1),
)

# display the figure
figure.show()