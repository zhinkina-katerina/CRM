import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
app = Celery('crm')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'dict': {
        'task': 'leads.tasks.create_object_order',
        'schedule': 50.0
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

