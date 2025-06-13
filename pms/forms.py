from datetime import datetime
from django import forms
from django.forms import ModelForm

from .models import Booking, Customer


class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout', 'guests']
        labels = {
            "guests": "Huéspedes"
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'max': datetime.today().replace(month=12, day=31).strftime('%Y-%m-%d')}),
            'guests': forms.DateInput(attrs={'type': 'number', 'min': 1, 'max': 4}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "name": "Nombre y apellido",
            "phone": "Teléfono"
        }


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests': forms.HiddenInput()
        }


class BookingFormExcluded(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer", "room", "code"]
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            'state': forms.HiddenInput(),
        }

class BookingDatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout', 'room']
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'checkout': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'room': forms.HiddenInput(),  
        }
        labels = {
            'checkin': 'Fecha de entrada',
            'checkout': 'Fecha de salida',
        }
        
    def __init__(self, *args, available_rooms=None, **kwargs):
        
        super().__init__(*args, **kwargs)

        if available_rooms is not None:
            self.fields['room'].widget = forms.Select(attrs={'class': 'form-select'})
            self.fields['room'].queryset = available_rooms
            self.fields['room'].initial = self.instance.room.pk
        
