from django.contrib import admin
from .models import User, Jsons, ForecastPoint, ForecastPoly


# Register your models here.
admin.site.register(ForecastPoint)
admin.site.register(ForecastPoly)
admin.site.register(User)
admin.site.register(Jsons)