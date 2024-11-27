#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import User, Jsons, ForecastPoint, ForecastPoly
from .converhex import convert_to_hex
from .serializer import ForecastPolySerializer, ForecastPointSerializer
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon

import json, requests, os, math
from django.core.serializers import serialize

from apscheduler.schedulers.blocking import BlockingScheduler
from itertools import chain



class PiontViewset(viewsets.ModelViewSet):
    serializer_class = ForecastPointSerializer
    def get_queryset(self):
        
        data = ForecastPoint.objects.all()
        print(data)
        return data
    

class WeatherViewset(viewsets.ModelViewSet):
    serializer_class = ForecastPolySerializer
    def get_queryset(self):
        
        data = ForecastPoly.objects.all()
         
        return data

    ## geting weather data from this api, you can change the date but not temprature
    def _get_weather_data(self):
        weather_url= "http://44.200.130.241:5000/forecast/20221112/NWS/temperature"
        api_request= requests.get(weather_url)

        try:
            api_request.raise_for_status()
            return api_request.json()
        except:
            return None

    def save_weather_data(self):
        test_api="/home/chris/visual/web50/final_project/cs50_weather/map/data/testapi.json"
        hexed_api="/home/chris/visual/web50/final_project/cs50_weather/map/geodata/testhex.geojson"
        weather_data = self._get_weather_data()
        ## if file exists allready, delete it
        if os.path.exists(test_api):
            os.remove(test_api)
            ## Create new geojson file 
            start_api_json=open(test_api, "w", encoding="utf-8")
            ## Load file with geo data 
            json.dump(weather_data, start_api_json, separators=(',', ':'))
            # Save
            start_api_json.close()
        else:
            ## Create new geojson file 
            start_api_json=open(test_api, "w", encoding="utf-8")
            ## Load file with geo data 
            json.dump(weather_data, start_api_json, separators=(',', ':'))
            # Save
            start_api_json.close()
        
        if weather_data is not None:
            try:
                convert_to_hex(weather_data)
                print("Data Hexed")
                with open(hexed_api) as json_file:
                    print("opened hex api")
                    output_file = json.load(json_file)
                    print("loaded hexapi")
                    for output in output_file['features']:
                        print(output)
                        print(output["geometry"]['type']) ## breaks here now
                        
                        if output["geometry"]['type']== "Point":
                            print(output["geometry"]['coordinates'])
                            weather_object = ForecastPoint(date = output["properties"]["date"], ## works
                                                                    location = output["properties"]["location"],
                                                                    active = output["properties"]["active"], ## works
                                                                    temp_max_forecast = output["properties"]["temp_max_forecast"] or None,
                                                                    temp_min_forecast = output["properties"]["temp_min_forecast"] or None,
                                                                    temp_max_observation = output["properties"]["temp_max_observation"] or None,
                                                                    temp_min_observation = output["properties"]["temp_min_observation"],
                                                                    bias_temp_max = output["properties"]["bias_temp_max"],
                                                                    bias_temp_min = output["properties"]["bias_temp_min"],
                                                                    to_date_rmse_temp_max = output["properties"]["to_date_rmse_temp_max"],
                                                                    to_date_rmse_temp_min = output["properties"]["to_date_rmse_temp_min"],
                                                                    _7_days_rmse_temp_max = output["properties"]["7_days_rmse_temp_max"],
                                                                    _7_days_rmse_temp_min = output["properties"]["7_days_rmse_temp_min"],
                                                                    _30_days_rmse_temp_max = output["properties"]["30_days_rmse_temp_max"],
                                                                    _30_days_rmse_temp_min = output["properties"]["30_days_rmse_temp_min"],
                                                                    geometry =  Point(output["geometry"]['coordinates'])
                                                                    )
                            print("weather object created")
                            weather_object.save()  
                            print("data saved in model") 


                        elif output["geometry"]['type']== "Polygon":
                            geom = (output["geometry"]['coordinates'][0])

                            print(geom)
                            weather_object = ForecastPoly(date = output["properties"]["date"],
                                                                    location = output["properties"]["location"],
                                                                    active = output["properties"]["active"],
                                                                    temp_max_forecast = output["properties"]["temp_max_forecast"],
                                                                    temp_min_forecast = output["properties"]["temp_min_forecast"],
                                                                    temp_max_observation = output["properties"]["temp_max_observation"],
                                                                    temp_min_observation = output["properties"]["temp_min_observation"],
                                                                    bias_temp_max = output["properties"]["bias_temp_max"],
                                                                    bias_temp_min = output["properties"]["bias_temp_min"],
                                                                    to_date_rmse_temp_max = output["properties"]["to_date_rmse_temp_max"],
                                                                    to_date_rmse_temp_min = output["properties"]["to_date_rmse_temp_min"],
                                                                    _7_days_rmse_temp_max = output["properties"]["7_days_rmse_temp_max"],
                                                                    _7_days_rmse_temp_min = output["properties"]["7_days_rmse_temp_min"],
                                                                    _30_days_rmse_temp_max = output["properties"]["30_days_rmse_temp_max"],
                                                                    _30_days_rmse_temp_min = output["properties"]["30_days_rmse_temp_min"],
                                                                    geometry =  Polygon(geom)
                                                                    )
                            print("weather object created")                                            
                            weather_object.save() 
                            print("data saved in model")
                        else:
                            print("Error: Not a Valid Geometry, must be polygon or point to load")
                            break

                        
            
            except:             
                pass
                #print("hexed api failed to save!")

        
            
## Redirects you to the url with the map
def index(request):
    return render(request, "map/weathermap.html" )

