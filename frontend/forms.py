# coding=utf-8
from django.contrib.auth.forms import PasswordChangeForm


class FrPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(PasswordChangeForm.error_messages, **{
        'password_incorrect': u"Votre ancien mot de passe n'est pas correct. Veuillez réessayer",
        'password_mismatch': u"Les deux mots de passe ne correspondent pas",
    })
