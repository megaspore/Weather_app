from shapely.geometry import shape, Point, Polygon
from pyproj import Proj, transform
import json, os, math



## pip install python-polylabel 
# for finding polygon center
from polylabel import polylabel
            


def convert_to_hex(weather_data):
    
    ### Working inline script to transform to hex
    print(weather_data)
    ## Backend api file
    apifile = "/home/chris/visual/web50/final_project/cs50_weather/map/data/testapi.json"
    ## Api expanded to area square used in this hexing script
    api_geo_json= "/home/chris/visual/web50/final_project/cs50_weather/map/geodata/test.geojson"
    ## State boundy geojson
    input = "/home/chris/visual/web50/final_project/cs50_weather/map/geodata/boundary.geojson"
    ## end hex geojson
    hex = "/home/chris/visual/web50/final_project/cs50_weather/map/geodata/testhex.geojson"



    input_file=json.load(open(apifile, "r", encoding="utf-8"))
    ## Geojson layout
    ## Defining a lat/log size vaiable to adjust the station size to minimize how many hexes its populates
    size=1
    geojs={
        "type": "FeatureCollection",
        "features":[
            {
                    
                    "type":"Feature",
                    "properties":d,
                    "geometry": {
                    "type":"Polygon",
                    ## Creat polygon from point
                    "coordinates":[[[transform(Proj(init="epsg:4326"), Proj(init="epsg:3857"), d["lon"]+size, d["lat"]),
                    transform(Proj(init="epsg:4326"), Proj(init="epsg:3857"), d["lon"], d["lat"]+size), 
                    transform(Proj(init="epsg:4326"), Proj(init="epsg:3857"), d["lon"]-size, d["lat"]), 
                    transform(Proj(init="epsg:4326"), Proj(init="epsg:3857"),d["lon"], d["lat"]-size)]]],
                },
                    
            ## Populate with inputfile data
            } for d in input_file 
        ]  
    }

    ## if file exists allready, delete it
    if os.path.exists(api_geo_json):
        os.remove(api_geo_json)
        ## Create new geojson file 
        newgeojson=open(api_geo_json, "w", encoding="utf-8")
        ## Load file with geo data 
        json.dump(geojs, newgeojson)
        # Save
        newgeojson.close()
    else:
        ## Create new geojson file 
        newgeojson=open(api_geo_json, "w", encoding="utf-8")
        ## Load file with geo data 
        json.dump(geojs, newgeojson)
        # Save
        newgeojson.close()

    input_geojson_file = (
        input #"boundary.geojson"  # polygon area of interest used for generating hexagons
    )
    r = 130000  # for the hexagon size


    # load the area of interest into a JSON object
    with open(input_geojson_file) as json_file:
        geojson = json.load(json_file)


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


    # create the hexagons
    for x in range(xmin, xmax, h): 
        print("creating hexigons....")
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


            print("hexigon FINISHED")
            # check if the hexagon is within the area of interest
            if polygon.intersects(hexagon):
                print("polygon intersects hexigon")
                date = ""
                location = ""
                active = 0
                temp_max_forecast = None
                temp_min_forecast = None
                temp_max_observation = None
                temp_min_observation = None
                bias_temp_max = None
                bias_temp_min = None
                to_date_rmse_temp_max =None
                to_date_rmse_temp_min = None
                seven_days_rmse_temp_max = None
                seven_days_rmse_temp_min = None
                thirty_days_rmse_temp_max = None
                thirty_days_rmse_temp_min = None
                

                
                # open the data points API geojson file
                with open(api_geo_json) as json_file:
                    print("opening api_geo_json")
                    geojson = json.load(json_file)
                    print("opened apigeojson")
                    ## Create new geojson file 

                    for feature in geojson["features"]:
                        
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
                            temp_max_forecast = feature["properties"]["temp_max_forecast"]
                            temp_min_forecast = feature["properties"]["temp_min_forecast"]

                            if feature["properties"]["temp_max_observation"] == 'None':
                                temp_max_observation = None
                            else:
                                temp_max_observation = feature["properties"]["temp_max_observation"]
                            
                            if feature["properties"]["temp_min_observation"] == 'None':
                                temp_min_observation = None
                            else:
                                temp_min_observation = feature["properties"]["temp_min_observation"]
                            
                            if feature["properties"]["bias_temp_max"] == 'None':
                               bias_temp_max = None
                            else:
                                bias_temp_max = feature["properties"]["bias_temp_max"]
                            if feature["properties"]["bias_temp_min"] =='None':
                                bias_temp_min = None
                            else:
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
                point = { 
                    
                    "type": "Feature",
                    "properties": {
                        "date" : date,
                        "location" : location,
                        "active" : active,
                        "temp_max_forecast" : temp_max_forecast,
                        "temp_min_forecast" : temp_min_forecast,
                        "temp_max_observation" : temp_max_observation,
                        "temp_min_observation":temp_min_observation,
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
                        # creating point at center of poly
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
                        "date"  :date,
                        "location" : location,
                        "active" : active,
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
                feature_collection["features"].append(point)
                feature_collection["features"].append(poly)

            i = math.floor((ymax - y) / r)
            offset = -h / 2 if i % 2 == 0 else h / 2


            x += offset

    ## if file exists allready, delete it
    if os.path.exists(hex):
        os.remove(hex)
        # output the feature collection to a geojson file
        with open(hex, "w") as output_file:
            output_file.write(json.dumps(feature_collection))
            output_file.close()
                
    else:
        with open(hex, "w") as output_file:
            output_file.write(json.dumps(feature_collection))
            output_file.close()
    print("done")
    print(output_file)
    return output_file
