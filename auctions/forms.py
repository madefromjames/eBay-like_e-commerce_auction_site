from django import forms
from django.contrib.auth.models import User

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
                'class': 'form-control', 'placeholder': 'Email'
            }),
        }
        help_texts = {
            'username': 'None'
        }

    def cleaned_data(self):
        password = self.cleaned_data.get('password')
        confirmation = self.cleaned_data.get('confirmation')

        if password and confirmation and password != confirmation:
            raise forms.ValidationError('Passwords do not match')
        else:
            return confirmation