#!/bin/bash

NAME='mavilla'

APP_BASE_DIR=/opt/mavilla/
VIRTUALENV_DIR=APP_BASE_DIR.venv/mavilla/bin

APP_DIR=$APP_BASE_DIR/src

cd $VIRTUALENV_DIR
source activate
cd $APP_DIR

export WORKON_HOME=/opt/mavilla/.venv/
export PYTHONPATH=$APP_DIR:$PYTHONPATH
exec celery -A historian worker -l info

