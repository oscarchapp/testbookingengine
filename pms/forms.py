from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Booking, Customer, Room


class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout", "guests"]
        labels = {"guests": "Huéspedes"}
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
            "guests": forms.DateInput(attrs={"type": "number", "min": 1, "max": 4}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {"name": "Nombre y apellido", "phone": "Teléfono"}


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        labels = {}
        widgets = {
            "checkin": forms.HiddenInput(),
            "checkout": forms.HiddenInput(),
            "guests": forms.HiddenInput(),
        }


class BookingEditForm(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer", "room", "code", "state", "total", "guests"]
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
        checkin = cleaned_data.get("checkin")
        checkout = cleaned_data.get("checkout")
        if (
            Booking.objects.filter(
                Q(checkin__range=(checkin, checkout))
                | Q(checkout__range=(checkin, checkout))
            )
            .exclude(state=Booking.DELETED)
            .exclude(code=self.instance.code)
            .exists()
        ):
            raise ValidationError("No hay disponibilidad para las fechas seleccionadas")


class BookingFormExcluded(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer", "room", "code"]
        labels = {}
        widgets = {
            "checkin": forms.HiddenInput(),
            "checkout": forms.HiddenInput(),
            "guests": forms.HiddenInput(),
            "total": forms.HiddenInput(),
            "state": forms.HiddenInput(),
        }

class RoomSearchNameForm(ModelForm):

    class Meta:
        model = Room
        exclude = ['room_type', 'description']
        labels = {
            "name": "Nombre de habitacion"
        }
        widgets = {
            'name': forms.TextInput()
        }

