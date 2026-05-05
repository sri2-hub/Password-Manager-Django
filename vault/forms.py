from django import forms
from .models import PasswordEntry

class PasswordEntryForm(forms.ModelForm):
    # Added plain_password field for the user to enter
    plain_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), 
        label="Password"
    )
    
    class Meta:
        model = PasswordEntry
        fields = ['service_name', 'username', 'plain_password']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Google'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., yourname@email.com'}),
        }