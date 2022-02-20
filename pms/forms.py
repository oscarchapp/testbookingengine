from django import forms
from django.forms import ModelForm
from .models import Book, Customer
from datetime import datetime
class RoomSearchForm(ModelForm):
    class Meta:
        model = Book
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

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests':forms.HiddenInput()
        }
    


class BookFormExcluded(ModelForm):
    class Meta:
        model = Book
        exclude = ["customer","code","room"]
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests':forms.HiddenInput(),
            'total':forms.HiddenInput()
        }
    
