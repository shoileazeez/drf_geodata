from django.apps import AppConfig
from .task import start_scheduler

class GeoDataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geo_data"

    def ready(self):
        start_scheduler()
