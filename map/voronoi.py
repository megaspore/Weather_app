#!/usr/bin/env python
# coding: utf-8

# In[1]:


from shapely.geometry import shape, Point, Polygon
from pyproj import Proj, transform
import json 
import math
from polylabel import polylabel
from shapely.geometry.polygon import Polygon
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
from geovoronoi import voronoi_regions_from_coords


# In[2]:


## Backend api file
apifile = "/home/ec2-user/API_Endpoint/20221229/NWS/temperature/api_endpoint_NWS_temperature_20221229.json"
input_geojson_file = "/home/ec2-user/production/weather/boundary.geojson"
input_file=json.load(open(apifile, "r", encoding="utf-8"))
with open(input_geojson_file) as json_file:
    geojson = json.load(json_file)


# In[3]:


input_geojson_file = gpd.read_file(input_geojson_file)

area = input_geojson_file.to_crs(epsg=3857)    # convert to World Mercator CRS
area_shape = area.iloc[0].geometry 


# In[4]:


df = pd.DataFrame(input_file)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
gdf = gdf.set_crs('epsg:4326')
gdf = gdf.to_crs(3857)


# In[5]:


region_polys, region_pts = voronoi_regions_from_coords(gdf['geometry'], area_shape)


# In[6]:


import matplotlib.pyplot as plt
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

fig, ax = subplot_for_map()
plot_voronoi_polys_with_points_in_area(ax, area_shape, region_polys, gdf['geometry'], region_pts)
plt.show()


# In[15]:


pol = []
for i in region_polys.values():
    
    if i.geom_type == 'Polygon':
        pol.append(i)
    elif i.geom_type == 'MultiPolygon':
        new_pol = []
        for j in i:
            new_pol.append(j.area)
            max_value = max(new_pol)
            if max_value == j.area:
                pol.append(j)
                print(j)
                print(max_value)
for i in pol:
    for j in range(len(gdf['geometry'])):
        if i.contains(gdf['geometry'][j]):
            gdf['geometry'][j] = i


# In[16]:


dict_json = gdf.to_json()
geojs = json.loads(dict_json)


# In[17]:


for i in geojs['features']:
    del i['id']


# In[18]:


for i in geojs['features']:
    coords = []
    for j in i['geometry']['coordinates'][0]:
        t = tuple(j)
        coords.append(t)
    
    i['geometry']['coordinates'] = [[coords]]


# In[19]:


geojs =  {"type": "FeatureCollection", "features": geojs['features']}


# In[22]:


r = 130000 


# In[23]:


# the area of interest coordinates (note this is for a single-part / contiguous polygon)
geographic_coordinates = geojson["features"][0]["geometry"]["coordinates"]
projected_coordinates = []


pt = transform(
    Proj(init="epsg:4326"),
    Proj(init="epsg:3857"),
    geographic_coordinates[0][0][0],
    geographic_coordinates[0][0][1],
)


# initialise the envelope extent parameters
xmin = int(pt[0])
ymin = int(pt[1])
xmax = int(pt[0])
ymax = int(pt[1])


# In[24]:


# calculate the actual envelope extent parameters
for coords in geographic_coordinates[0]:
    projected = transform(
        Proj(init="epsg:4326"), Proj(init="epsg:3857"), coords[0], coords[1]
    )
    projected_coordinates.append([projected[0], projected[1]])
    xmin = int(projected[0]) if projected[0] < xmin else xmin
    ymin = int(projected[1]) if projected[1] < ymin else ymin
    xmax = int(projected[0]) if projected[0] > xmax else xmax
    ymax = int(projected[1]) if projected[1] > ymax else ymax


# create an area of interest polygon using shapely
polygon = shape({"type": "Polygon", "coordinates": [projected_coordinates]})


# twice the height of a hexagon's equilateral triangle
h = int(r * math.sqrt(3))


# create the feature collection - empty geojson object
feature_collection = {"type": "FeatureCollection", "features": []}


# In[25]:


# create the hexagons
for x in range(xmin, xmax, h):
    for y in range(ymin, ymax, int(h * h / r / 2)):
        hexagon = shape(
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [x, y + r],
                                [x + h / 2, y + r / 2],
                                [x + h / 2, y - r / 2],
                                [x, y - r],
                                [x - h / 2, y - r / 2],
                                [x - h / 2, y + r / 2],
                                [x, y + r],
                            ]
                        ],
                    }
                )


        # check if the hexagon is within the area of interest
        if polygon.intersects(hexagon):
            date = ""
            location = ""
            s_id = ""
            active = 0
            temp_max_forecast = 0
            temp_min_forecast = 0
            temp_max_observation = 0
            temp_min_observation = 0
            bias_temp_max = 0
            bias_temp_min = 0
            to_date_rmse_temp_max = 0
            to_date_rmse_temp_min = 0
            seven_days_rmse_temp_max = 0
            seven_days_rmse_temp_min = 0
            thirty_days_rmse_temp_max = 0
            thirty_days_rmse_temp_min = 0

            for feature in geojs["features"]:
                state = shape(
                            {
                                "type": "Polygon",
                                "coordinates": feature["geometry"]["coordinates"][0],
                            }
                        )

                        # check if hexagon is within the state and add properties to that hex
                if hexagon.intersects(state):
                    date = feature["properties"]["date"]
                    location = feature["properties"]["location"]
                    active = 1
                    s_id = str(int(feature["properties"]['lat'])) + str(int(abs(feature["properties"]["lon"])))
                    temp_max_forecast = feature["properties"]["temp_max_forecast"]
                    temp_min_forecast = feature["properties"]["temp_min_forecast"]
                    temp_max_observation = feature["properties"]["temp_max_observation"]
                    temp_min_observation = feature["properties"]["temp_min_observation"]
                    bias_temp_max = feature["properties"]["bias_temp_max"]
                    bias_temp_min = feature["properties"]["bias_temp_min"]
                    try:
                        to_date_rmse_temp_max = feature["properties"]["to_date_rmse_temp_max"]
                        to_date_rmse_temp_min = feature["properties"]["to_date_rmse_temp_min"]
                    except:
                        to_date_rmse_temp_max = None
                        to_date_rmse_temp_min = None                            
                    try:
                        thirty_days_rmse_temp_max = feature["properties"]["30_days_rmse_temp_max"]
                        thirty_days_rmse_temp_min = feature["properties"]["30_days_rmse_temp_min"]
                    except:
                        thirty_days_rmse_temp_max  = None
                        thirty_days_rmse_temp_min = None
                    try:
                        seven_days_rmse_temp_max = feature["properties"]["7_days_rmse_temp_max"]
                        seven_days_rmse_temp_min = feature["properties"]["7_days_rmse_temp_min"]
                    except:
                        seven_days_rmse_temp_max = None
                        seven_days_rmse_temp_min = None


            # Convert the coordinates back to EPSG 4326
            coords1 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x, y + r
                        )
            coords2 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x + h / 2, y + r / 2
                        )
            coords3 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x + h / 2, y - r / 2
                        )
            coords4 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x, y - r
                        )
            coords5 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x - h / 2, y - r / 2
                        )
            coords6 = transform(
                            Proj(init="epsg:3857"), Proj(init="epsg:4326"), x - h / 2, y + r / 2
                        )


            # create the intersecting feature
            feature = { 

                            "type": "Feature",
                            "properties": {
                                "date" : date,
                                "location" : location,
                                'active': active,
                                's_id': s_id,
                                "temp_max_forecast" : temp_max_forecast,
                                "temp_min_forecast" : temp_min_forecast,
                                "temp_max_observation" : temp_max_observation,
                                "temp_min_observation" : temp_min_observation,
                                "bias_temp_max" : bias_temp_max,
                                "bias_temp_min" : bias_temp_min,
                                "to_date_rmse_temp_max" : to_date_rmse_temp_max,
                                "to_date_rmse_temp_min" : to_date_rmse_temp_min,
                                "7_days_rmse_temp_max" : seven_days_rmse_temp_max,
                                "7_days_rmse_temp_min" : seven_days_rmse_temp_min,
                                "30_days_rmse_temp_max" : thirty_days_rmse_temp_max,
                                "30_days_rmse_temp_min" : thirty_days_rmse_temp_min,
                            },

                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": polylabel([
                                    [
                                        [coords1[0], coords1[1]],
                                        [coords2[0], coords2[1]],
                                        [coords3[0], coords3[1]],
                                        [coords4[0], coords4[1]],
                                        [coords5[0], coords5[1]],
                                        [coords6[0], coords6[1]],
                                        [coords1[0], coords1[1]],
                                    ]
                                ]),
                            },
                        }
            poly = { 

                "type": "Feature",
                "properties": {
                                "date" : date,
                                "location" : location,
                                'active': active,
                                's_id': s_id,
                                "temp_max_forecast" : temp_max_forecast,
                                "temp_min_forecast" : temp_min_forecast,
                                "temp_max_observation" : temp_max_observation,
                                "temp_min_observation" : temp_min_observation,
                                "bias_temp_max" : bias_temp_max,
                                "bias_temp_min" : bias_temp_min,
                                "to_date_rmse_temp_max" : to_date_rmse_temp_max,
                                "to_date_rmse_temp_min" : to_date_rmse_temp_min,
                                "7_days_rmse_temp_max" : seven_days_rmse_temp_max,
                                "7_days_rmse_temp_min" : seven_days_rmse_temp_min,
                                "30_days_rmse_temp_max" : thirty_days_rmse_temp_max,
                                "30_days_rmse_temp_min" : thirty_days_rmse_temp_min,
                },

                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [coords1[0],coords1[1]],
                            [coords2[0],coords2[1]],
                            [coords3[0],coords3[1]],
                            [coords4[0],coords4[1]],
                            [coords5[0],coords5[1]],
                            [coords6[0],coords6[1]],
                            [coords1[0],coords1[1]],
                        ]
                    ],    
                },
            }

            # add the feature to the feature collection
            feature_collection["features"].append(feature)
            feature_collection["features"].append(poly)

        i = math.floor((ymax - y) / r)
        offset = -h / 2 if i % 2 == 0 else h / 2


        x += offset


# In[26]:


path = '/home/ec2-user/tryfile3.geojson'
f = open(path, 'w+')
f.write(json.dumps(feature_collection))
f.close()


# In[ ]:




