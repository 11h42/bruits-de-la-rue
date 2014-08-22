# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

from core.models import Bid, BidCategories, EmergencyLevels


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['name', 'type', 'begin', 'end', 'status', 'quantity', 'real_author',
                  'emergency_level',
                  'description', 'bidCategory', 'photo', 'quantity_type', 'adress1', 'adress2', 'zipcode',
                  'town', 'country', 'photo']

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['bidCategory'].choices = [(Category.id, Category.bid_category_name) for Category in
                                              BidCategories.objects.all()]
        self.fields['emergency_level'].choices = [(Emergency.id, Emergency.name) for Emergency in
                                              EmergencyLevels.objects.all()]



    TYPES = (('Offre', 'Offre', ), ('Demande', 'Demande', ))
    type = forms.ChoiceField(widget=forms.Select, choices=TYPES)

    TYPES_QUANTITES = (('KG', 'KG', ), ('Unitaire', 'Unitaire', ), ('Litres', 'Litres'), ('Autre', 'Autre', ))
    quantity_type = forms.ChoiceField(widget=forms.Select, choices=TYPES_QUANTITES)

    TYPES_STATUS = (('En cours', 'En cours', ), ('Accepté', 'Accepté', ), ('Fermé', 'Fermé', ), ('Expiré', 'Expiré', ))
    status = forms.ChoiceField(widget=forms.Select, choices=TYPES_STATUS)


    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            if Image.open(photo).size > (512, 512):
                raise ValidationError("Votre image est trop grande (Dimensions max : 512x512 pixels)")
            return photo