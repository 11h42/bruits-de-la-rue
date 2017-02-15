# Dépot Application Action Association


## requirements

 * python 3


## virtualenv and dependencies

   python3 -m venv venv
   source venv\bin\activate
   python -m pip install -r requirements.txt

## tests

    python manage.py test

## run server

    python manage.py migrate
    python manage.py runserver


## load static file in dev mode

set `debug = True` in `config/config.ini` file

    [DJANGO]
    ...
    debug = True

## debug email

add `debug_email = True` in `config/config.ini` file

    [DJANGO]
    ...
    debug_email = True