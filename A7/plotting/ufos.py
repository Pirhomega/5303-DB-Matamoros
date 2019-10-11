import numpy as np
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
ufos = db["ufos"]

data = [go.Scattermapbox(lat = ufos["latitude"])]