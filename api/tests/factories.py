# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import factory

from core.models.models import Bid, User, BidCategories, EmergencyLevels


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = "factory_user@akema.fr"
    password = factory.PostGenerationMethodCall('set_password',
                                                'password')
    first_name = "factory"
    last_name = "user"
    username = "userFactory"

    is_donor = False
    is_admin = False
    is_active = True


class BidCategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = BidCategories

    bid_category_name = "Alimentaire"
    bid_category_description = "Une catégorie d'annonce créée via factory"


class EmergencyLevelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EmergencyLevels

    name = "URGENT"
    level = 10


class BidFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Bid

    name = "Factored Bid"
    caller = factory.SubFactory(UserFactory)
    acceptor = None
    begin = datetime.today()
    end = datetime.today() + timedelta(days=2)
    quantity = 20
    adress1 = "Impasse de la factory"
    adress2 = "BP3902"
    zipcode = "12345"
    town = "Factory-Town"
    country = "Factory-Country"
    photo = 'images/default.png'
    real_author = "factories.py"

    description = "Ceci est la description d'une annonce créée via factory"
    bidCategory = factory.SubFactory(BidCategoryFactory)
    quantity_type = "KG"
    status = "En cours"
    type = "Offre"
    emergency_level = factory.SubFactory(EmergencyLevelFactory)