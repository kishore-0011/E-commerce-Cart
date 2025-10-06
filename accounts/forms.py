from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '1234567890'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Tailwind classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })

        # Username placeholder and help
        self.fields['username'].widget.attrs.update({
            'placeholder': 'johndoe'
        })
        
        # Password placeholders
        self.fields['password1'].widget.attrs.update({
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '••••••••'
        })

        # Remove Django's default help texts
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check if username contains only letters
        if not re.match(r'^[A-Za-z]+$', username):
            raise ValidationError('Username must contain only letters (no numbers or special characters).')
        
        # Check length
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        
        if len(username) > 30:
            raise ValidationError('Username must be less than 30 characters.')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if phone:
            # Remove any spaces or dashes
            phone = phone.replace(' ', '').replace('-', '')
            
            # Check if it's exactly 10 digits
            if not re.match(r'^\d{10}$', phone):
                raise ValidationError('Phone number must be exactly 10 digits.')
        
        return phone

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Minimum length check
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one letter
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one letter.')
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Passwords do not match.')
        
        return password2


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Invalid username or password. Please try again.',
        'inactive': 'This account is inactive.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Tailwind classes
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '••••••••'
        })