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


# By Nauzet

class DateEditBooking(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        labels = {
            "checkin": "Checkin",
            "checkout": "Checkout"
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'max': datetime.today().replace(month=12, day=31).strftime('%Y-%m-%d')}),
        }

    def __init__(self, *args, **kwargs):
        super(DateEditBooking, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    def cleanDateEdit(self):
        clean_data = super().clean()
        checkin = clean_data['checkin']
        checkout = clean_data['checkout']
        date_booking = Booking.objects.exclude(id=self.instance.pk).filter(checkin__lt=checkout, checkout__gt=checkin)
        if date_booking.exists():
            raise forms.ValidationError("Ya existe una reserva en ese rango de fechas")
        return clean_data

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






