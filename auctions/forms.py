from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
    