from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    title = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    town = models.CharField(max_length=255)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipient_name': self.recipient_name,
            'address1': self.address1,
            'address2': self.address2,
            'zipcode': self.zipcode,
            'town': self.town
        }

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Adresse"


class DatedModel(models.Model):
    """ An abstract base class for models that needs date
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Faq(DatedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def serialize(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }


class User(AbstractUser, DatedModel):
    addresses = models.ManyToManyField("Address", blank=True, null=True)

    class Meta:
        verbose_name = "Utilisateur"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_superuser': self.is_superuser,
            'is_staff': self.is_staff,
        }


class Association(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=15, blank=True, null=True)
    url_site = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    administrator = models.ForeignKey(User, blank=True, null=True, related_name='associations_administrated',
                                      on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, blank=True, null=True, related_name='associations')

    def serialize(self, with_members=False):
        address = self.address.serialize() if self.address else None
        administrator = self.administrator.serialize() if self.administrator else None
        association = {
            'id': self.id,
            'name': self.name,
            'address': address,
            'phone': self.phone,
            'url_site': self.url_site,
            'email': self.email,
            'administrator': administrator
        }
        if with_members:
            members = []
            for member in self.members.all():
                members.append(member.serialize())
            association['members'] = members
        return association

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "Association"


class BidCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "Catégorie d'une annonce"
        verbose_name_plural = "Catégories des annonces"


class TypeBids(object):
    SUPPLY = 'SUPPLY'
    DEMAND = 'DEMAND'
    TYPE_CHOICES = (
        (SUPPLY, _('Supply')),
        (DEMAND, _('Demand')),
    )


class StatusBids(object):
    ONHOLD = u'EN ATTENTE'
    CLOSED = u'FERME'
    ACCEPTED = u'ACCEPTE'
    RUNNING = u'EN COURS'
    TYPE_CHOICES = (
        (CLOSED, _('Closed')),
        (ACCEPTED, _('Accepted')),
        (RUNNING, _('Running')),
        (ONHOLD, _('On hold')),
    )


class Photo(models.Model):
    photo = models.FileField(upload_to="photos/")
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.id


class Bid(models.Model):
    creator = models.ForeignKey(User, related_name='bids_created')
    purchaser = models.ForeignKey(User, related_name='bids_accepted', null=True, blank=True, on_delete=models.SET_NULL)

    begin = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    quantity = models.IntegerField(null=True, blank=True)
    localization = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)

    description = models.TextField()
    title = models.CharField(max_length=255)

    category = models.ForeignKey(BidCategory, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(choices=TypeBids.TYPE_CHOICES,
                            default=TypeBids.SUPPLY,
                            max_length=20)

    status_bid = models.CharField(choices=StatusBids.TYPE_CHOICES,
                                  default=StatusBids.RUNNING,
                                  max_length=20)

    real_author = models.CharField(blank=True, null=True, max_length=255)

    association = models.ForeignKey(Association, blank=True, null=True, on_delete=models.SET_NULL)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)

    def serialize(self):
        # creator = self.creator.username if self.creator else None
        # purchaser = self.purchaser.username if self.purchaser else None
        begin = self.begin.isoformat() if self.begin else None
        end = self.end.isoformat() if self.end else None
        category = self.category.serialize() if self.category else None
        localization = self.localization.serialize() if self.localization else None
        association = self.association.serialize() if self.association else None
        photo = self.photo.id if self.photo else None
        return {
            'id': self.id,
            'title': self.title,
            'begin': begin,
            'end': end,
            'quantity': self.quantity,
            'description': self.description,
            'creator': self.creator.username,
            'category': category,
            'type': self.type,
            'real_author': self.real_author,
            'localization': localization,
            'status_bid': self.status_bid,
            'association': association,
            'photo': photo
        }

    def __str__(self):
        return u'%s' % self.title

    def belong_to_user(self, user):
        return self.creator == user

    class Meta:
        verbose_name = "Annonce"