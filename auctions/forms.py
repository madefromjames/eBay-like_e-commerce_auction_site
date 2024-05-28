from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Listing, Bid, Comment

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password'
        }),
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.',
        }
    )
    confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Confirmation'
        }),
        error_messages={
            'required': 'Password confirmation is required.',
        }
    )

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
        error_messages = {
            'username': {
                'required': 'Username is required.',
                'max_length': 'Username must be less than 150 characters.',
                'unique': 'Username already exists.',
            },
            'email': {
                'invalid': 'Enter a valid email address.',
            },
        }
        help_texts = {
            'username': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

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

class addBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Bid Price', 'step': '0.01'
            })
        }
        error_messages = {
            'bid': {
                'required': 'Bid amount is required.'
            },
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Add your Comment',
                'maxlength': '100'
            })
        }
        error_messages = {
            'message': {
                'required': 'Comment is required.',
                'max_length': 'Comment must be less than 100 characters.'
            },
        }

        def clean_message(self):
            message = self.cleaned_data.get('message', '').strip()
            if not message:
                raise forms.ValidationError("Comment is required.")
            return message