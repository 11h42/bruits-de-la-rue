# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
    association_fk_association = models.ManyToManyField('Association', null=True)
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


class Message(models.Model):
    from_user_fk_user = models.ForeignKey(User, related_name='from_user_fk_user')
    to_user_fk_user = models.ForeignKey(User, related_name='to_user_fk_user')
    read = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('message-details', kwargs={'pk': self.pk})


class Bid(models.Model):
    caller_fk_user = models.ForeignKey(User, related_name='caller_fk_user')
    acceptor_fk_user = models.ForeignKey(User, related_name='acceptor_fk_user', null=True)
    type = models.CharField(max_length=10)
    begin = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=200, decimal_places=20, null=True, blank=True)
    localization = models.CharField(max_length=255)
    real_author = models.CharField(max_length=255)
    emergency_level = models.CharField(max_length=255)
    recurrence = models.BooleanField(default=False)
    description = models.TextField()
    name = models.CharField(max_length=255)
    bidCategory = models.CharField(max_length=255)
    photo = models.FileField(upload_to='uploads/photos', blank=True, null=True)
    type_quantite = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('core:bid-details', args=(self.pk, ))