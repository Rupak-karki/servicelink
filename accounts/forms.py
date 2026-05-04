from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Optional: Your phone number'
    }))
    user_type = forms.ChoiceField(choices=[
        ('customer', 'I need services (Customer)'),
        ('provider', 'I offer services (Provider)')
    ], widget=forms.RadioSelect, initial='customer'
    # , help_text="Choose whether you want to explore services or provide them."
    # error_messages={
    #      'required': "Please select whether you’re a customer or provider."
    #     }
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields

        #username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })

        #password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        
        # Customize help text
        self.fields['username'].help_text = 'Please choose a unique username.'

        self.fields['email'].help_text = 'Please enter a valid email address. We will never share your email with anyone else.' 

        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

        # self.fields['password2'].help_text = "Re-enter the same password for confirmation."