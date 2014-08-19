# -*- coding: utf-8 -*-
from django import forms
from core.models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['name', 'type', 'begin', 'end', 'status', 'quantity', 'localization', 'real_author',
                  'emergency_level',
                  'recurrence', 'description', 'bidCategory', 'photo', 'type_quantite']

    TYPES = (('Offre', 'Offre', ), ('Demande', 'Demande', ))
    type = forms.ChoiceField(widget=forms.Select, choices=TYPES)

    TYPES_QUANTITES = (('KG', 'KG', ), ('Unitaire', 'Unitaire', ), ('Litres', 'Litres'), ('Autre', 'Autre', ))
    type_quantite = forms.ChoiceField(widget=forms.Select, choices=TYPES_QUANTITES)