import os
from celery import Celery
import django

# set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

app = Celery("config")

#Load settings from Django settings.py, using `CELERY_` namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

#Auto-discover tasks from all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")