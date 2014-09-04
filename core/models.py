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


class Association(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    url_site = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)


class DatedModel(models.Model):
    """ An abstract base class for models that needs date
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, DatedModel):
    associations = models.ManyToManyField('Association', blank=True, null=True)


class BidCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class TypeBids(object):
    SUPPLY = 'SUPPLY'
    DEMAND = 'DEMAND'
    TYPE_CHOICES = (
        (SUPPLY, _('Supply')),
        (DEMAND, _('Demand')),
    )


class StatusBids(object):
    CLOSED = 'CLOSED'
    ACCEPTED = 'ACCEPTED'
    RUNNING = 'RUNNING'
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

    def serialize(self):
        # creator = self.creator.username if self.creator else None
        # purchaser = self.purchaser.username if self.purchaser else None
        begin = self.begin.isoformat() if self.begin else None
        end = self.end.isoformat() if self.end else None
        category = self.category.name if self.category else None

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
        }

    def __unicode__(self):
        return u'%s' % self.title