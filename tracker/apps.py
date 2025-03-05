# tracker/apps.py
from django.apps import AppConfig
import threading
from django.conf import settings

class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"

    def ready(self):
        # Only start the background task in production (or customize as needed)
        if settings.DEBUG:
            from .utils import price_check_loop
            threading.Thread(target=price_check_loop, daemon=True).start()
