# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    recipient_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.IntegerField(max_length=10)
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

    def __unicode__(self):
        return u'%s' % self.title


class Association(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    url_site = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    def serialize(self):
        address = self.address.serialize() if self.address else None
        return {
            'id': self.id,
            'name': self.name,
            'address': address,
            'phone': self.phone,
            'fax': self.fax,
            'url_site': self.url_site,
            'email': self.email
        }

    def __unicode__(self):
        return u'%s' % self.name


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
            'question': self.question,
            'answer': self.answer
        }


class User(AbstractUser, DatedModel):
    associations = models.ManyToManyField('Association', blank=True, null=True)
    address = models.ManyToManyField('Address', blank=True, null=True)

    class Meta:
        verbose_name = "Utilisateur"


class BidCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "Catégorie d'une annonce"
        verbose_name_plural = "Catégorie d'une annonce"


class TypeBids(object):
    SUPPLY = 'SUPPLY'
    DEMAND = 'DEMAND'
    TYPE_CHOICES = (
        (SUPPLY, _('Supply')),
        (DEMAND, _('Demand')),
    )


class StatusBids(object):
    CLOSED = u'Ferme'
    ACCEPTED = u'Accepte'
    RUNNING = u'En cours'
    TYPE_CHOICES = (
        (CLOSED, _('Closed')),
        (ACCEPTED, _('Accepted')),
        (RUNNING, _('Running')),
    )


class Bid(models.Model):
    creator = models.ForeignKey(User, related_name='creators')
    purchaser = models.ForeignKey(User, related_name='purchasers', null=True, blank=True)

    begin = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    quantity = models.IntegerField(null=True, blank=True)
    localization = models.ForeignKey(Address, null=True, blank=True)

    description = models.TextField()
    title = models.CharField(max_length=255)

    category = models.ForeignKey(BidCategory, blank=True, null=True)
    type = models.CharField(choices=TypeBids.TYPE_CHOICES,
                            default=TypeBids.SUPPLY,
                            max_length=20)

    status = models.CharField(choices=StatusBids.TYPE_CHOICES,
                              default=StatusBids.RUNNING,
                              max_length=20)

    real_author = models.CharField(blank=True, null=True, max_length=255)

    association = models.ForeignKey(Association, blank=True, null=True)

    def serialize(self):
        # creator = self.creator.username if self.creator else None
        # purchaser = self.purchaser.username if self.purchaser else None
        begin = self.begin.isoformat() if self.begin else None
        end = self.end.isoformat() if self.end else None
        category = self.category.serialize() if self.category else None
        localization = self.localization.serialize() if self.localization else None
        association = self.association.serialize() if self.association else None
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
            'status': self.status,
            'association': association
        }

    def __unicode__(self):
        return u'%s' % self.title