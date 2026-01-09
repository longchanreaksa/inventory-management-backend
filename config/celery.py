import os
from celery import Celery

# Tell Celery to use Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('inventory-management-system')

# Load settings with CELERY_ prefix from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all apps
app.autodiscover_tasks()
