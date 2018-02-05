#!/bin/bash

NAME='mavilla'

APP_BASE_DIR=/opt/mavilla/
VIRTUALENV_DIR=APP_BASE_DIR.venv/mavilla/bin

APP_DIR=$APP_BASE_DIR/src

# configure the sock file. create the directory if necessary
SOCK_FILE=$APP_BASE_DIR/gunicorn.sock
RUN_DIR=$(dirname $SOCK_FILE)
test -d $RUN_DIR || mkdir -p $RUN_DIR

# configure the log file. create the directory if necessary
LOG_FILE=$APP_BASE_DIR/logs/supervisor-$NAME.log
LOG_DIR=$(dirname $LOG_FILE)
test -d $LOG_DIR || mkdir -p $LOG_DIR

NUM_WORKERS=4

cd $VIRTUALENV_DIR
source activate
cd $APP_DIR

export WORKON_HOME=/opt/mavilla/.venv/
export PYTHONPATH=$APP_DIR:$PYTHONPATH

exec gunicorn historian.website:flask_app \
	--worker-class eventlet \
	--workers $NUM_WORKERS \
    --log-level=debug \
	--bind 0.0.0.0:5000 \
    --timeout 500
	--reload
