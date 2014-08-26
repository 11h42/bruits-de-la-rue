# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.transaction import commit_on_success_unless_managed


class Association(models.Model):
    name = models.CharField(max_length=255)
    adress = models.TextField()
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    url_site = models.CharField(max_length=255)
    contact_mail = models.CharField(max_length=255)
    schedule = models.TextField()

    def get_absolute_url(self):
        return reverse('association-details', kwargs={'pk': self.pk})


class DatedModel(models.Model):
    """ An abstract base class for models that needs datation
    """
    # inner stuff
    created = models.DateTimeField(
        "Créé le",
        auto_now_add=True
    )

    modified = models.DateTimeField(
        "Dernière modification le",
        auto_now=True
    )

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, company and password.
        """
        if not email:
            raise ValueError('Un utilisateur doit forcement posseder une adresse mail')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser with the given email and password"""

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, DatedModel):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True, db_index=True)
    first_name = models.CharField(verbose_name='Prénom', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='Nom', max_length=30, blank=True)
    username = models.CharField(verbose_name='Nom d\'utilisateur', max_length=30, unique=True)
    associations = models.ManyToManyField('Association', null=True)
    is_donor = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('utilisateur-details', kwargs={'pk': self.pk})

    def get_user_associations(self):
        return Association.objects.filter()


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_fk_user')
    to_user = models.ForeignKey(User, related_name='to_user_fk_user')
    read = models.BooleanField(default=False)
    message = models.TextField()

    def get_absolute_url(self):
        return reverse('message-details', kwargs={'pk': self.pk})


class BidCategories(models.Model):
    bid_category_name = models.CharField(blank=False, null=False, unique=True, max_length=255)
    bid_category_description = models.TextField(blank=True, null=True)


def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.caller_fk_user.username, filename)


class EmergencyLevels(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    level = models.IntegerField()


def clean_serialize(data):
    if data['end'] and data['begin']:
        data['time_left'] = data['end'] - data['begin']

    if data['time_left']:
        data['time_left'] = str(data['time_left'])

    if data['end']:
        data['end'] = data['end'].isoformat()
    if data['begin']:
        data['begin'] = data['begin'].isoformat()

    return data


def bid_json_valid(bid):
    # todo check if the json is valid
    Bid(caller=User.objects.get(id=bid['caller']), name=str(bid['name']), real_author=str(bid['real_author']),
        description=str(bid['description']), bidCategory=BidCategories.objects.get(name=bid['bidCategory']),
        type=bid['type'], emergency_level=EmergencyLevels.objects.get(level=bid['emergency_level_level'])).save(
        commit_on_success_unless_managed())

    return True


class Bid(models.Model):
    caller = models.ForeignKey(User, related_name='caller_fk_user')
    acceptor = models.ForeignKey(User, related_name='acceptor_fk_user', null=True)

    begin = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    # todo decimal
    quantity = models.IntegerField(null=True, blank=True)
    adress1 = models.CharField(max_length=255, null=True, blank=True)
    adress2 = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.IntegerField(max_length=8, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    real_author = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255)

    bidCategory = models.ForeignKey(BidCategories)

    photo = models.FileField(upload_to=upload_to, blank=True, null=True)
    quantity_type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    emergency_level = models.ForeignKey(EmergencyLevels)

    def serialize(self):
        """Serialize Bid object"""
        caller = self.caller.username if self.caller else None
        acceptor = self.acceptor.username if self.acceptor else None
        end = self.end.isoformat() if self.end else None
        begin = self.begin.isoformat() if self.begin else None
        # todo add base64 photo

        data = {'id': self.id, 'name': self.name, 'begin': self.begin, 'end': self.end, 'quantity': self.quantity,
                'quantity_type': self.quantity_type, 'emergency_level': self.emergency_level.id, 'status': self.status}

        return clean_serialize(data)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('api:get-bid', args=(self.pk, ))