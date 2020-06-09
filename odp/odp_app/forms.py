from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm as DefaultSetPasswordForm
from django.contrib.auth import  password_validation

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

class PasswordResetForm(forms.Form):
        email = forms.EmailField(required=True, help_text="Inserisci la mail con il quale l'utente è registrato.")

class SetPasswordForm(forms.Form):
        """
        Even though this form  is present in the dafault,
        it strangely prompts for the user to be chosen, because it
        requires a user object.
        """
        error_messages = {
        'password_mismatch': 'Le due password non coincidono',
        }

        new_password1 = forms.CharField(
                label='Nuova password',
                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                strip=False,
        )
        new_password2 = forms.CharField(
                label='Conferma',
                strip=False,
                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )

        def clean_new_password2(self):
                password1 = self.cleaned_data.get('new_password1')
                password2 = self.cleaned_data.get('new_password2')
                if password1 and password2:
                        if password1 != password2:
                                raise forms.ValidationError(
                                self.error_messages['password_mismatch'],
                                code='password_mismatch',
                                )
                        password_validation.validate_password(password2) #difference with default is here!
                        return password2
