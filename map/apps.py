from django.apps import AppConfig


class MapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map'

    def ready(self):
        print("Starting Scheduler ...")
        from . import  weather_updater
        weather_updater.start()