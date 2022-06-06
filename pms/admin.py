from django.contrib import admin

from .models import Room, Booking, Customer, Room_type

admin.site.register([Room, Booking, Customer, Room_type])
