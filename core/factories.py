import factory

from models import User


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