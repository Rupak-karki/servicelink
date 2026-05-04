from django import forms
from .models import Booking

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