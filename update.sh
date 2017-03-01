#!/usr/bin/env bash
git pull origin master
source env/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic