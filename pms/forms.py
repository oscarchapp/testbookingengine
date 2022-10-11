from django import forms
from django.forms import ModelForm
from .models import Booking, Customer
from datetime import datetime
class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout', 'guests']
        labels = {
            "guests":"Huéspedes"
            }
        widgets = {
            'checkin': forms.DateInput(attrs = {'type':'date','min':datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(attrs = {'type':'date','max':datetime.today().replace(month = 12, day = 31).strftime('%Y-%m-%d')}),
            'guests': forms.DateInput(attrs = {'type':'number','min':1,'max':4}),
            }
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "name":"Nombre y apellido",
            "phone":"Teléfono"
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
            'guests':forms.HiddenInput()
        }


class BookingFormExcluded(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer","room","code"]
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests':forms.HiddenInput(),
            'total':forms.HiddenInput(),
            'state':forms.HiddenInput(),
        }

class BookingFormDates(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout"]
        widgets = {
            'checkin': forms.DateInput(attrs = {'type':'date','min':datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(attrs = {'type':'date','max':datetime.today().replace(year=2022, month=12, day=31).strftime('%Y-%m-%d')}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['checkin'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['checkout'].widget.attrs.update({'class': 'form-control w-50'})

    
