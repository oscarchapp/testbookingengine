from django import forms
from django.forms import ModelForm
from .models import Book, Customer

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields="__all__"
        labels={
        }
class BookForm(ModelForm):
    class Meta:
        model=Book
        fields="__all__"
        labels={
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests':forms.HiddenInput()
        }
    


class BookFormExcluded(ModelForm):
    class Meta:
        model=Book
        exclude=["customer","code","room"]
        labels={
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests':forms.HiddenInput()
        }
    
