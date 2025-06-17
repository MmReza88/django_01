from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    codice_fiscale = forms.CharField(max_length=64, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'codice_fiscale']