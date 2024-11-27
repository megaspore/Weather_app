from apscheduler.schedulers.background import BackgroundScheduler
from .views import WeatherViewset

## Background scheduler to automaticly import api data at a certain time
def start():
    schedular = BackgroundScheduler()
    weather = WeatherViewset()
    schedular.add_job(weather.save_weather_data, "interval", minutes=2, id="weather_001", replace_existing=True)
    # unhash below to start background scheduler
    #schedular.start()