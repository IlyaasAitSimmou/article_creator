from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        label="Password"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError("The password you entered is incorrect.")
        return password
