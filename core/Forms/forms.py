# -*- coding: utf-8 -*-
from django import forms
from core.models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['name', 'type', 'begin', 'end', 'status', 'quantity', 'real_author',
                  'emergency_level',
                  'recurrence', 'description', 'bidCategory', 'photo', 'quantity_type', 'adress1', 'adress2', 'zipcode',
                  'town', 'country']

    TYPES = (('Offre', 'Offre', ), ('Demande', 'Demande', ))
    type = forms.ChoiceField(widget=forms.Select, choices=TYPES)

    TYPES_QUANTITES = (('KG', 'KG', ), ('Unitaire', 'Unitaire', ), ('Litres', 'Litres'), ('Autre', 'Autre', ))
    quantity_type = forms.ChoiceField(widget=forms.Select, choices=TYPES_QUANTITES)