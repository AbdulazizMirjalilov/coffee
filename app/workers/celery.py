from celery import Celery

from app.core.config import settings

BROKER_URL = settings.CELERY_BROKER_URL
CELERY_RESULT_URL = settings.CELERY_RESULT_BACKEND

celery = Celery("worker", broker=BROKER_URL, backend=CELERY_RESULT_URL)

celery.conf.broker_connection_retry_on_startup = True
celery.autodiscover_tasks(["app.tasks"])
