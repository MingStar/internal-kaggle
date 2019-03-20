#!/bin/sh

if [ "$RUN_MODE" == 'WORKER' ]
then
    celery -A run.celery worker --loglevel=$LOG_LEVEL
elif [ "$RUN_MODE" == 'MONITOR' ]
then
    flower -A run.celery --port=5555 --broker=$CELERY_BROKER_URL --persistent=True --db=/flower/flower.db
else
    uwsgi --ini uwsgi.ini
fi
