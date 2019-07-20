#!/bin/bash
export FLASK_RUN_PORT=5000
export FLASK_APP=app.py
export FLASK_ENV=development

source env/bin/activate

flask run --host 0.0.0.0


unset FLASK_RUN_PORT
unset FLASK_APP
