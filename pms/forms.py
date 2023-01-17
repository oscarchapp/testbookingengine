from datetime import datetime, date
from django import forms
from django.forms import ModelForm

from .models import Booking, Customer, Room


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


class EditReservationDatesForm(forms.ModelForm):
    checkin = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']

        def clean(self):
            cleaned_data = super().clean()
            checkin = cleaned_data.get("checkin")
            checkout = cleaned_data.get("checkout")
            room_id = self.initial["room"]
            if checkin and checkout:
                if checkin >= checkout:
                    self.add_error('checkout', 'La fecha de salida debe ser mayor que la de entrada')
                if checkin < date.today():
                    self.add_error('checkin', 'La fecha de entrada no puede ser en el pasado')
                if Room.objects.filter(id=room_id, booking__checkin__range=(checkin, checkout)
                 | Q(booking__checkout__range=(checkin, checkout))).exists():
                    self.add_error('checkin', 'La habitación no está disponible en las fechas seleccionadas')