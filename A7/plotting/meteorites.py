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
me = db["meteorites"]

# iterate through mongodb collection and create a pandas dataframe with the collection data
cursor_meteorites = me.find()
df = pd.DataFrame(list(cursor_meteorites))

# sets the geospatial data up
figure = go.Figure(go.Scattermapbox(lat = df["reclat"], 
                                    lon = df["reclong"],
                                    text = df["name"],
                                    mode = "markers",   
                                    marker=dict(size=4,color="yellow",opacity=.8)
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
    title="Meteor strikes around the world")

# displays the data using the default renderer
figure.show()