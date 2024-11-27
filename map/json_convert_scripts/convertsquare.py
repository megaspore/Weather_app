import json
input = "/home/chris/visual/bengie/weather/map/data/api_endpoint_OWM_temperature_20221010.json"
output = "/home/chris/visual/bengie/weather/map/geodata/test.geojson"
input_file=json.load(open(input, "r", encoding="utf-8"))
# Converts data to a square

geojs={
    "type": "FeatureCollection",
    "features":[
        {
                
                "type":"Feature",                
                "geometry": {
                "type":"Polygon",
                "coordinates":[[[d["lon"]+1, d["lat"]], [d["lon"], d["lat"]+1], [d["lon"]-1, d["lat"]], [d["lon"], d["lat"]-1]]],
            },
                "properties":d,
        
        } for d in input_file 
    ]  
}

newgeojson=open(output, "w", encoding="utf-8")
json.dump(geojs, newgeojson)


newgeojson.close()