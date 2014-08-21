# Register your models here.
from django.db.models import get_models, get_app
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin

app_models = get_app('core')

for model in get_models(app_models):
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass