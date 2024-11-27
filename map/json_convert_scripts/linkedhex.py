from shapely.geometry import shape, Point, Polygon
from pyproj import Proj, transform
import json 
import math
        
### Working on a inline script to transform to hex



input = "/home/chris/visual/bengie/weather/map/geodata/boundary.geojson"
## Output variable, what populates the map currently
output = "/home/chris/visual/bengie/weather/map/geodata/test.geojson"
## Hex variable is the output ran through pyEAC tesillation, currently not working dynamicly
hex = "/home/chris/visual/bengie/weather/map/geodata/testhex.geojson"
statejson= "/home/chris/visual/bengie/weather/map/geodata/us_states1.geojson"

input_geojson_file = (
    input #"boundary.geojson"  # polygon area of interest used for generating hexagons
)
r = 50000  # for the hexagon size


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
            population = 0
            state_name = ""


            # open the US states geojson file
            with open(statejson) as json_file:
                geojson = json.load(json_file)


                for feature in geojson["features"]:
                    state = shape(
                        {
                            "type": "Polygon",
                            "coordinates": feature["geometry"]["coordinates"][0],
                        }
                    )


                    # check if hexagon is within the state and derive the population for that intersected part of the hexagon
                    if hexagon.intersects(state):
                        state_name = "{} ({})".format(
                            feature["properties"]["NAME"],
                            feature["properties"]["POPULATION"],
                        )


                        population += (
                            hexagon.intersection(state).area
                            / state.area
                            * feature["properties"]["POPULATION"]
                        )


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
                    "name": state_name,
                    "population": population,
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [coords1[0], coords1[1]],
                            [coords2[0], coords2[1]],
                            [coords3[0], coords3[1]],
                            [coords4[0], coords4[1]],
                            [coords5[0], coords5[1]],
                            [coords6[0], coords6[1]],
                            [coords1[0], coords1[1]],
                        ]
                    ],
                },
            }


            # add the feature to the feature collection
            feature_collection["features"].append(feature)


        i = math.floor((ymax - y) / r)
        offset = -h / 2 if i % 2 == 0 else h / 2


        x += offset


# output the feature collection to a geojson file
with open(hex, "w") as output_file:
    output_file.write(json.dumps(feature_collection))


print("done")