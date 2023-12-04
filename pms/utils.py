from django.db.models import Q

from .models import Booking
from .managers import BookingManager, RoomManager


class Utils:
    @staticmethod
    def get_occupancy_percentage():
        """
        Returns the occupancy percentage as a float number
        """
        confirmed_bookings = BookingManager().get_confirmed_bookings_count()

        room_count = RoomManager().get_room_count()

        return 0 if room_count == 0 else (confirmed_bookings / room_count) * 100

