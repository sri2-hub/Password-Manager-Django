from django import forms
from .models import PasswordEntry

class PasswordEntryForm(forms.ModelForm):
    # Added plain_password field for the user to enter
    plain_password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = PasswordEntry
        fields = ['service_name', 'username']