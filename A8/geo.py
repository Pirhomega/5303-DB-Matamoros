import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]

mapbox_access_token = "pk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uMGhsMzAwMGszaW11OXZhempxMTMifQ.tQp7BareQGxwalQvIQvBsw"

def get_within_box(collection,bbox):
    min_lon = bbox['min_lon']
    max_lon = bbox['max_lon']
    min_lat = bbox['min_lat']
    max_lat = bbox['max_lat']

    results = []

    for res in db[collection].find({"loc": { "$geoWithin": { "$box":  [ [ min_lon, max_lat ], [ max_lon, min_lat ] ] } }}):
        results.append(res)

    return results

# searches for the argument sent into parameter 'country' in the database
# returns country document 
def get_country_geojson(country):
    global db
    countries = db["countries"]

    geo = countries.find({"properties.ADMIN" : country})

    return geo

# returns dictionary called points filled with country border lats and lons
def get_country_border(country):
    global db
    countries = db["countries"]

    lines = []
    points = {'lat':[],'lon':[],'lonlat':[]}

    # grab data from the database and stick it into a list called 'lines'.
    for obj in countries.find({"properties.ADMIN" : country}, { "geometry.type" : 1, "geometry.coordinates": 1, "_id": 0 }):
        lines.append(obj)
    
    if lines[0]["geometry"]["type"] == "Polygon":
        for group in lines[0]['geometry']['coordinates']:
            #print(group)
            for line in group:
                #print(line)
                points['lat'].append(float(line[1]))
                points['lon'].append(float(line[0]))
                points['lonlat'].append((float(line[0]),float(line[1])))
    else:
        for group in lines[0]['geometry']['coordinates']:
            #print(group)
            for line in group:
                #print(line)
                for point in line:
                    points['lat'].append(float(point[1]))
                    points['lon'].append(float(point[0]))
                    points['lonlat'].append((float(point[0]),float(point[1])))

    return points

def get_center_point(points):
    min_lat = 90
    max_lat = -90
    min_lon = 180
    max_lon = -180

    for point in points:
        if point[1] < min_lat:
            min_lat = point[1]
        if point[0] < min_lon:
            min_lon = point[0]
        if point[1] > max_lat:
            max_lat = point[1]
        if point[0] > max_lon:
            max_lon = point[0]

    return {"lon":(min_lon + max_lon)/2,"lat":(min_lat + max_lat)/2}

# returns dictionary of the bounding points of a country
def get_bbox(points):
    min_lat = 90.0
    max_lat = -90.0
    min_lon = 180.0
    max_lon = -180.0
    
    for point in points['lonlat']:
        #print(point)
        if float(point[1]) < min_lat:
            min_lat = float(point[1])
        if float(point[0]) < min_lon:
            min_lon = float(point[0])
        if float(point[1]) > max_lat:
            max_lat = float(point[1])
        if float(point[0]) > max_lon:
            max_lon = float(point[0])

    return {"lon":(min_lon + max_lon)/2,"lat":(min_lat + max_lat)/2,"min_lat":min_lat,"max_lat":max_lat,"min_lon":min_lon,"max_lon":max_lon}

def draw_bbox(bbox):
    lats = []
    lons = []
    lats.append(bbox['max_lat'])
    lons.append(bbox['min_lon'])
    lats.append(bbox['max_lat'])
    lons.append(bbox['max_lon'])
    lats.append(bbox['min_lat'])
    lons.append(bbox['max_lon'])
    lats.append(bbox['min_lat'])
    lons.append(bbox['min_lon'])
    lats.append(bbox['max_lat'])
    lons.append(bbox['min_lon'])
    return lats,lons


def within_bbox(bbox,lat,lon):
    return (lat < bbox['max_lat'] and lat > bbox['min_lat'] and lon < bbox['max_lon'] and lon > bbox['min_lon'])

def get_meteorites():
    meteors = db["meteorites"]
    lats = []
    lons = []
    for obj in meteors.find():
        latlon = obj['GeoLocation'][1:-1]
        if len(latlon.strip()) > 0:
            lat,lon = latlon.split(',')
            lat = float(lat)
            lon = float(lon)
            #if within_bbox(bbox,lat,lon):
            lats.append(lat)
            lons.append(lon)
    return (lats,lons)


def get_ufos():
    ufos = db["ufos"]
    lats = []
    lons = []
    for obj in ufos.find():
        lat = float(obj['latitude'])
        lon = float(obj['longitude'])
        #if within_bbox(bbox,lat,lon):
        lats.append(lat)
        lons.append(lon)
    return (lats,lons)