from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.db.models import Q
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


class BookingEditDatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(
                attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        self.booking = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        checkin = self.cleaned_data.get('checkin')
        checkout = self.cleaned_data.get('checkout')
        if checkout < checkin:
            self.add_error('checkout', "checkout invalid")
        room = self.booking.room
        booking_exist = (
            Booking.objects
            .exclude(id=self.booking.id)
            .filter(room=room, state=Booking.NEW)
            .filter(
                Q(checkin__range=[checkin, checkout]) | 
                Q(checkout__range=[checkin, checkout])
            )
        )
        if booking_exist.exists():
            raise forms.ValidationError("Booking already exists with date")
        return self.cleaned_data