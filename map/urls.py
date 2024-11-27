from django.urls import path, include, re_path

from . import views
from rest_framework.routers import DefaultRouter
from .views import WeatherViewset, PiontViewset

router = DefaultRouter()
router.register("polys", WeatherViewset, basename="weather-data")
router.register("points", PiontViewset, basename="points-data" )
## urls to map and geojson
urlpatterns = [
    re_path("routes/", include(router.urls)),
    path("", views.index, name="index"), 
    ## test url before api  
    #path("geofile", views.geofile, name="geofile"),
]