import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_USER = os.environ.get('RABBIT_USER')
RABBIT_PASS = os.environ.get('RABBIT_PASS')

CELERY_BROKER_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASS}@localhost//'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
