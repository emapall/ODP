from django import forms
from django.contrib.auth.forms import UserCreationForm

from odp_app.models import User
class SignupForm(UserCreationForm):
    email = forms.EmailField(label="Indirizzo email", required=True)
    first_name = forms.CharField(label="Nome/i", max_length=100, required=True)
    last_name = forms.CharField(label="Cognome/i", max_length=100, required=True)

    class Meta:
        model = User
        fields = (
                "first_name",
                "last_name",
                "email",
                "username",
                "password1",
                "password2",
            )
        labels = {
                # "first_name":"Nome/i",
                # "last_name":"Cognome",
                # "email":"Indirizzo email",
                "username":"Username (da utilizzare per il login)",
                "password1":"Password",
                "password2":"Conferma pasword",
        }
        help_texts = {
                "password1":"Almeno 8 caratteri, non torppo comune.",
                "password2":None,
        }
