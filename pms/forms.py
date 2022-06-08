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


class BookingCustomForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        widgets = {
            'checkin': forms.DateInput(attrs = {
                'class':'form-control',
                'type':'date',
                'min':datetime.today().strftime('%Y-%m-%d')
            }),
            'checkout': forms.DateInput(attrs = {
                'class':'form-control',
                'type':'date',
                'min':datetime.today().strftime('%Y-%m-%d'),
                'max':datetime.today().replace(month = 12, day = 31).strftime('%Y-%m-%d')})
            }

    # def clean(self):
    #     query = self.cleaned_data
    #     checkin = query.get('checkin')
    #     checkout = query.get('checkout')
    #     booking_room = self.instance.room
    #     booking = Booking.objects.filter(
    #         Q(checkin__gte=checkin) and
    #         Q(checkout__lte=checkout) and
    #         Q(room__name=booking_room)).values()[0]

    #     if booking["checkin"] == checkin or booking["checkout"] != checkout and booking["room"] == booking_room:
    #         raise forms.ValidationError("Ya existe una reserva con esas caracteristicas.")
    #     return query