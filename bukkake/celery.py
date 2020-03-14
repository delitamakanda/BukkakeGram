from __future__ import absolute_import, unicode_literals
from decouple import config
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('tasks', broker=config('REDISTOGO_URL'))

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, prune.s(), name="Prune users", expires=10)

@app.task
def prune():
    from channels_presence.models import Room
    Room.objects.prune_presences()
