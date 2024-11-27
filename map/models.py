from django.db import models
from django.contrib.gis.db import models
# "pip install django-jsonfield" :for jsonfield


from django.contrib.auth.models import AbstractUser
# Create your models here.

# creating users & superuser list for backend 
class User(AbstractUser):
    pass

# storing json file and converted geojson // this is not used at the moment
class Jsons(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    the_json = models.JSONField()
    the_geojson = models.JSONField(null=True)

# Storing point data
class ForecastPoint(models.Model):
    date = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=500, blank=True)
    active = models.IntegerField(null=True, blank=True)
    temp_max_forecast = models.IntegerField(null=True, blank=True)
    temp_min_forecast = models.IntegerField(null=True, blank=True)
    temp_max_observation = models.IntegerField(null=True, blank=True)
    temp_min_observation = models.IntegerField(null=True, blank=True)
    bias_temp_max = models.IntegerField(null=True, blank=True)
    bias_temp_min = models.IntegerField(null=True, blank=True)
    to_date_rmse_temp_max = models.IntegerField(null=True, blank=True)
    to_date_rmse_temp_min = models.IntegerField(null=True, blank=True)
    _7_days_rmse_temp_max = models.IntegerField(null=True, blank=True)
    _7_days_rmse_temp_min = models.IntegerField(null=True, blank=True)
    _30_days_rmse_temp_max = models.IntegerField(null=True, blank=True)
    _30_days_rmse_temp_min = models.IntegerField(null=True, blank=True)
    geometry = models.PointField( null=True, blank=True)
    
    
    def __str__(self):
        return "{} at {}".format(self.date, self.location)

# Storing polygon data
class ForecastPoly(models.Model):
    date = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=500, blank=True)
    active = models.IntegerField(null=True, blank=True)
    temp_max_forecast = models.IntegerField(null=True, blank=True)
    temp_min_forecast = models.IntegerField(null=True, blank=True)
    temp_max_observation = models.IntegerField(null=True, blank=True)
    temp_min_observation = models.IntegerField(null=True, blank=True)
    bias_temp_max = models.IntegerField(null=True, blank=True)
    bias_temp_min = models.IntegerField(null=True, blank=True)
    to_date_rmse_temp_max = models.IntegerField(null=True, blank=True)
    to_date_rmse_temp_min = models.IntegerField(null=True, blank=True)
    _7_days_rmse_temp_max = models.IntegerField(null=True, blank=True)
    _7_days_rmse_temp_min = models.IntegerField(null=True, blank=True)
    _30_days_rmse_temp_max = models.IntegerField(null=True, blank=True)
    _30_days_rmse_temp_min = models.IntegerField(null=True, blank=True)
    geometry = models.PolygonField(null=True, blank=True)
    
    def __str__(self):
        return "{} at {}".format(self.date, self.location)
