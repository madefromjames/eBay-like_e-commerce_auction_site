from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Listing

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirmation'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Email (Optional)'
            }),
        }
        help_texts = {
            'username': None
        }

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirmation = self.cleaned_data.get('confirmation')

        if password and confirmation and password != confirmation:
            raise ValidationError('Passwords do not match')
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'imageUrl', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Title'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Description'
            }),
            'imageUrl': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Image URL'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'
            }),
        }
        error_messages = {
            'title': {
                'required': 'Title is required.',
                'max_length': 'Title must be less than 100 characters.'
            },
            'description': {
                'required': 'Description is required.',
            },
            'price': {
                'required': 'Price is required.',
                'invalid': 'Enter a valid price.'
            },
        }