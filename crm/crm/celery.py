import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
app = Celery('crm')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_object_order': {
        'task': 'leads.tasks.create_object_order',
        'schedule': 300.0
    },
    'upgrade_ttn_information': {
        'task': 'leads.tasks.upgrade_ttn_information',
        'schedule': 86400.0
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

