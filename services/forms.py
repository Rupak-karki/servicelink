from django import forms
from .models import Booking, Service, Category

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'special_requests']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests? (e.g., need parking, bring specific tools, etc.)'
            }),
        }
        labels = {
            'booking_date': 'Preferred Date & Time',
            'special_requests': 'Special Requests (Optional)'
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category', 'location', 'image', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Emergency Plumbing Service'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service in detail...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in NPR'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kathmandu, Baneshwor'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['is_available'].initial = True