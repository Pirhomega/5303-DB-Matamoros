import plotly
import plotly.graph_objects as go
import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
planes = db["plane_crashes"]

plane_cursor = planes.find()
df = pd.DataFrame(list(plane_cursor))
plane_300_lat = []
plane_300_lon = []
plane_300_count = []
plane_200_lat = []
plane_200_lon = []
plane_200_count = []
plane_100_lat = []
plane_100_lon = []
plane_100_count = []
plane_0_lat = []
plane_0_lon = []
plane_0_count = []

# divides plane data into catagories based on fatality count
for obj in planes.find():
    if int(obj["TotalFatalInjuries"]) > 300: # add all crashes with 300 or more fatalities
        plane_300_lat.append(float(obj["Latitude"]))
        plane_300_lon.append(float(obj["Longitude"]))
        plane_300_count.append(obj["TotalFatalInjuries"])
    elif int(obj["TotalFatalInjuries"]) > 200: # add all crashes with 200 or more fatalities
        plane_200_lat.append(float(obj["Latitude"]))
        plane_200_lon.append(float(obj["Longitude"]))
        plane_200_count.append(obj["TotalFatalInjuries"])
    elif int(obj["TotalFatalInjuries"]) > 100: # add all crashes with 100 or more fatalities
        plane_100_lat.append(float(obj["Latitude"]))
        plane_100_lon.append(float(obj["Longitude"]))
        plane_100_count.append(obj["TotalFatalInjuries"])
    elif int(obj["TotalFatalInjuries"]) > -1: # add all crashes with 0 or more fatalities
        plane_0_lat.append(float(obj["Latitude"]))
        plane_0_lon.append(float(obj["Longitude"]))
        plane_0_count.append(obj["TotalFatalInjuries"])

figure = go.Figure()

# sets the geospatial data up for all crash categories above
figure.add_trace(go.Scattermapbox(  lat = plane_300_lat, 
                                    lon = plane_300_lon,
                                    text = plane_300_count,
                                    mode = "markers",   
                                    marker={'color':'red','size':30}
                                    )
                                )
figure.add_trace(go.Scattermapbox(  lat = plane_200_lat, 
                                    lon = plane_200_lon,
                                    text = plane_200_count,
                                    mode = "markers",   
                                    marker={'color':'orange','size':25}
                                    )
                                )
figure.add_trace(go.Scattermapbox(  lat = plane_100_lat, 
                                    lon = plane_100_lon,
                                    text = plane_100_count,
                                    mode = "markers",   
                                    marker={'color':'yellow','size':20}
                                    )
                                )
figure.add_trace(go.Scattermapbox(  lat = plane_0_lat, 
                                    lon = plane_0_lon,
                                    text = plane_0_count,
                                    mode = "markers",   
                                    marker={'color':'blue','size':15}
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
    title="Deadly Plane Crashes around the World")

# displays the data using the default renderer
figure.show(renderer="iframe")