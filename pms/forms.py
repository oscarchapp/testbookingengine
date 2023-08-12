from datetime import datetime
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


def get_first_equal_room_available(checkin, checkout, room_type):
    """Get first room available for the given dates and room type"""

    # get available rooms and total according to dates and guests
    filters = {
        'room_type': room_type
    }
    exclude = {
        'booking__checkin__lte': checkout,
        'booking__checkout__gte': checkin,
        'booking__state__exact': "NEW"
    }
    return (
        Room.objects
        .filter(**filters)
        .exclude(**exclude)
        .order_by("room_type__max_guests", "name").first()
    )

class BookingDatesForm(ModelForm):

    def clean(self):
        # Get clean data
        cleaned_data = super().clean()

        # Get checkin and checkout
        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')

        # Get new room
        if checkin and checkout:
            new_room = get_first_equal_room_available(
                checkin=checkin,
                checkout=checkout,
                room_type=self.instance.room.room_type
            )
            if new_room:
                self.instance.room = new_room
            else:
                raise forms.ValidationError(
                    "No hay disponibilidad para las fechas seleccionadas."
                )
        else:
            raise forms.ValidationError(
                "Es necesario proporcionar una fecha de entrada y una fecha de salida."
            )

        return cleaned_data

    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}
            ),
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
