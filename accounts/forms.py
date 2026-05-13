from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserProfile


# ==============================
# 1. Custom Registration Form
# ==============================
class CustomRegistrationForm(UserCreationForm):
    """Registration form with email, phone, and user type selection"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text="Please enter a valid email address. We will never share your email."
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional: Your phone number'
        })
    )

    user_type = forms.ChoiceField(
        choices=[
            ('customer', 'I need services (Customer)'),
            ('provider', 'I offer services (Provider)')
        ],
        widget=forms.RadioSelect,
        initial='customer',
        help_text="Choose whether you want to explore services or provide them."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Add Bootstrap styling and customize help texts"""
        super().__init__(*args, **kwargs)

        # Username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['username'].help_text = 'Please choose a unique username.'

        # Password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        self.fields['password2'].help_text = "Re-enter the same password for confirmation."


# ==============================
# 2. User Update Form
# ==============================
class UserUpdateForm(forms.ModelForm):
    """Form for updating basic User model fields"""

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ==============================
# 3. Profile Update Form
# ==============================
class ProfileUpdateForm(forms.ModelForm):
    """Form for updating extended UserProfile fields"""

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your location/address'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell customers about your services...'
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
