from datetime import datetime, timedelta
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


class BookingDatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout"]
        labels = {
            "checkin": "Check in",
            "checkout": "Check out",
        }
        widgets = {
            'checkin': forms.widgets.DateInput(attrs={"type": "date"}),
            'checkout': forms.widgets.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        """
        Make sure the dates are not in the range of some other bookings with a state of 'NEW' on the same room

        Example:
            Given the next data, here's example of the cases
            Booking:
                checkin = 20 April 2000
                checkout = 25 April 2000

        NOT VALID
        18 - 22 / 19 - 26 Q(checkin__range=(check_in, check_out - timedelta(days=1)))
        21 - 27 / 19 - 26 Q(checkout__range=(check_in + timedelta(days=1), check_out))
        22 - 23 Q(checkin__lte=check_in, checkout__gte=check_out)

        VALID
        19 - 20 Q(checkin__range=(check_in, check_out - timedelta(days=1)))
        25 - 27 Q(checkout__range=(check_in + timedelta(days=1), check_out))

        """

        cleaned_data = super().clean()
        check_in = cleaned_data.get("checkin")
        check_out = cleaned_data.get("checkout")

        if check_in == check_out:
            raise forms.ValidationError("Check out can't be same day as check in.")

        if Booking.objects.filter(
                ~Q(id=self.instance.id) &
                Q(state=Booking.NEW) &
                Q(room=self.instance.room) &
                Q(
                    Q(
                        Q(checkin__range=(check_in, check_out - timedelta(days=1))) |
                        Q(checkout__range=(check_in + timedelta(days=1), check_out))
                      ) |
                    Q(checkin__lte=check_in, checkout__gte=check_out)
                )
        ).exists():
            raise forms.ValidationError("No hay disponibilidad para las fechas seleccionadas.")
        return cleaned_data

    def save(self, commit=True):
        check_in = self.cleaned_data.get("checkin")
        check_out = self.cleaned_data.get("checkout")

        time_spent = check_out - check_in
        room_price = self.instance.room.room_type.price

        self.instance.total = time_spent.days * room_price
        self.instance.save()

        return super().save(commit=commit)




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
