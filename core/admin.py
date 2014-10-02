from django import forms
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from core.models import User, BidCategory, Association, Faq, Address


admin.site.unregister(Group)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'is_staff')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                'email', 'first_name', 'username', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(BidCategory)
admin.site.register(Association)
admin.site.register(Address)
admin.site.register(Faq)

LogEntry.objects.all().delete()