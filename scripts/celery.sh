#!/bin/sh
exec celery -A app.workers.celery.celery worker --loglevel=info
