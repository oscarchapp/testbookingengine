from datetime import datetime
from django import forms
from django.forms import ModelForm

from .form_dates.dates_limits import *
from .models import Booking, Customer


class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout', 'guests']
        labels = {
            "guests": "Huéspedes"
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': get_today_str()}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'max': get_checkout_max_date(), 'min': get_checkout_min_date()}),
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


class DatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        labels = {
            'checkin': 'Checkin',
            'checkout': 'Checkout'
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': get_today_str()}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'max': get_checkout_max_date(), 'min': get_checkout_min_date()}
            )
        }
