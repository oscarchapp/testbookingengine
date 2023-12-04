from django.db import models, transaction

from .models import Room, Booking

class BookingManager(models.Manager):

    def get_confirmed_bookings_count(self):
        """
        Return count of confirmed bookings(state=NEW)
        """
        return Booking.objects.filter(state=Booking.NEW).count()

class RoomManager(models.Manager):

    def get_room_count(self):
        """
        Return count of total rooms
        """
        return Room.objects.count()
