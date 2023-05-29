#!/bin/sh
cd src
celery -A shipping.settings.celery_app.app worker --loglevel=info