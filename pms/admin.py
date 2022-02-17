from django.contrib import admin

from .models import Room, Book, Customer, Room_type
# Register your models here.

admin.site.register([Room, Book, Customer,Room_type])