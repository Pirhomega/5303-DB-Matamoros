import plotly
import plotly.graph_objects as go
import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
volcanos = db["volcanos"]

# iterate through mongodb collection and create a pandas dataframe with the collection data
cursor_volcanos = volcanos.find().sort([('PEI', -1)])
df = pd.DataFrame(list(cursor_volcanos))

figure = go.Figure()

# sets the geospatial data up
figure.add_trace(go.Scattermapbox(lat = df["latitude"][:3], 
                                    lon = df["longitude"][:3],
                                    text = df["V_Name"][:3],
                                    mode = "markers",   
                                    marker={'color':['red','orange','yellow'],'size':[30, 20, 10]}
                                    )
                                )

# sets the geospatial data up
figure.add_trace(go.Scattermapbox(lat = df["latitude"][3:], 
                                    lon = df["longitude"][3:],
                                    text = df["V_Name"][3:],
                                    mode = "markers",   
                                    marker=dict(size=5,symbol='mountain')
                                    )
                                )

# sets the layout for plotting
figure.update_layout(
    autosize = True,
    hovermode="closest",
    template="plotly_dark",
    mapbox = go.layout.Mapbox(  accesstoken = "pk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uMGhsMzAwMGszaW11OXZhempxMTMifQ.tQp7BareQGxwalQvIQvBsw",
                                bearing = 0,
                                center = go.layout.mapbox.Center(lat = 33.9137, lon = -98.4934),
                                pitch = 0,
                                zoom = 5),
    title="Volcano eruptions around the world")

# displays the data using the default renderer
figure.show(renderer='iframe')