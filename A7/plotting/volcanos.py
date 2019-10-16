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
vo = db["volcanos"]

# iterate through mongodb collection and create a pandas dataframe with the collection data
cursor_volcanos = vo.find()
df = pd.DataFrame(list(cursor_volcanos))
df2 = pd.DataFrame(list(df["properties"]))

# sets the geospatial data up
figure = go.Figure(go.Scattermapbox(lat = df2["Latitude"], 
                                    lon = df2["Longitude"],
                                    text = df2["V_Name"],
                                    mode = "markers",   
                                    marker=dict(size=4,color="red",opacity=.8)
                                    )
                                )

# sets the layout for plotting
figure.update_layout(
    autosize = True,
    hovermode="closest",
    template="plotly_dark",
    mapbox = go.layout.Mapbox(  accesstoken=mapbox_token,
                                bearing = 0,
                                center = go.layout.mapbox.Center(lat = 33.9137, lon = -98.4934),
                                pitch = 0,
                                zoom = 5),
    title="Volcano eruptions around the world")

# displays the data using the default renderer
figure.show()