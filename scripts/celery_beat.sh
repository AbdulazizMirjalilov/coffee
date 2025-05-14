#!/bin/sh
exec celery -A app.workers.celery.celery beat --loglevel=info
