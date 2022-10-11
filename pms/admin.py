from django.contrib import admin

from .models import Room, Booking, Customer, Room_type
# Register your models here.

admin.site.register([Room, Booking, Customer,Room_type])