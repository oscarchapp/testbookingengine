from datetime import datetime
from django import forms
from django.db.models import Q
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


class BookingUpdateDateForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout"]
        labels = {}
        widgets = {
            "checkin": forms.DateInput(
                attrs={"type": "date", "min": datetime.today().strftime("%Y-%m-%d")}
            ),
            "checkout": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": datetime.today()
                    .replace(month=12, day=31)
                    .strftime("%Y-%m-%d"),
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        checkin = cleaned_data["checkin"]
        checkout = cleaned_data["checkout"]
        reservation = Booking.objects.filter(
            Q(checkin__range=(checkin, checkout)) |
            Q(checkout__range=(checkin, checkout)),
            room_id=instance.room.id
        ).exclude(
            id=instance.id
        )
        if reservation:
            raise forms.ValidationError(
                "No hay disponibilidad para las fechas seleccionadas"
            )
        return cleaned_data