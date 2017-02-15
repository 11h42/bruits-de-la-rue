from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm

from core import models


class UserChangeForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30, help_text='')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = 'True'

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('Sauvegarder', 'Sauvegarder'))

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name')


class NewUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': "Un utilisateur avec le même nom existe",
    }
    username = forms.RegexField(label="Nom d'utilisateur", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Obligatoire. 30 caractères ou moins",
                                error_messages={'invalid': "Ce nom d'utilisateur n'est pas bon"})

    email = forms.EmailField(required=True, help_text="Obligatoire.", )
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    is_public_member = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('Créer un nouvel utilisateur', 'Créer un nouvel utilisateur'))

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password')
        labels = {
            'username': "Nom de l'utilisateur",
            'email': "Email",
            'first_name': "Prénom",
            'last_name': "Nom",
            'password': 'Mot de passe',
            'is_public_member': "Membre validé",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'], code='duplicate_username', )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_public_member = self.cleaned_data['is_public_member']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PasswordChangeFormFR(PasswordChangeForm):
    error_messages = dict(PasswordChangeForm.error_messages, **{
        'password_incorrect': u"Votre ancien mot de passe n'est pas correct. Veuillez réessayer",
        'password_mismatch': u"Les deux mots de passe ne correspondent pas",
    })

    def __init__(self, *args, **kwargs):
        super(PasswordChangeFormFR, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('Sauvegarder', 'Sauvegarder'))


class AssociationForm(ModelForm):
    class Meta:
        model = models.Association
        fields = ('name', 'phone', 'url_site', 'email')
        labels = {
            'name': "Nom de l'association",
            'phone': "Téléphone",
            'url_site': "Site internet",
        }
        widgets = {
            'administrator': forms.widgets.Select(choices=models.User.objects.all())
        }

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('Sauvegarder', 'Sauvegarder'))
