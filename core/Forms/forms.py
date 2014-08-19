# -*- coding: utf-8 -*-
from django import forms


class OffersForm(forms.Form):
    bid_name = forms.CharField(label='Titre de l\'annonce', max_length=255)
    bid_quantity = forms.DecimalField(label='Quantité' )
    bid_category = forms.ChoiceField()
    bid_comment = forms.CharField(widget=forms.widgets.Textarea())
    bid_dlc = forms.DateField()

    def validate_bid_name(self):
        data = self.cleaned_data['bid_name']
        return data

    def validate_bid_quantity(self):
        data = self.cleaned_data['bid_quantity']
        return data

    def validate_bid_category(self):
        data = self.cleaned_data['bid_category']
        return data

    def validate_bid_comment(self):
        data = self.cleaned_data['bid_comment']
        return data

    def validate_bid_dlc(self):
        data = self.cleaned_data['bid_dlc']
        return data


    def create_offer(request):
        pass