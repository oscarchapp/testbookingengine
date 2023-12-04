import datetime

from django.db.models import Q

from .models import Booking
from .exceptions import InvalidDateError, NoAvailabilityError
from .managers import BookingManager


class Utils:

    @staticmethod
    def check_room_availability(booking, checkin, checkout):
        """
        Check room availability:
        - First check if dates are valid (checkout date > checkin date). If not valid, raise and exception to
        inform the user
        - Filter occupied rooms in the entered range of dates. The interval in the filter is
        because the same day may be a checkout and a checkin. The filter excludes the same room, because if it is
        the same customer, the room would be free in those dates
        - If there are occupied rooms in the range, raise an exception with the message to inform the user
        """
        total_days = checkout - checkin
        if total_days < 1:
            raise InvalidDateError("La fecha del checkout debe ser mayor a la del checkin")

        occupied_rooms = Booking.objects.filter(
            Q(checkin__range=(checkin.date, checkout.date + datetime.timedelta(days=-1))) | Q(
                checkout__range=(checkin.date + datetime.timedelta(days=1), checkout.date)), room=booking.room, state=Booking.NEW).exclude(
            id=booking.id)

        if len(occupied_rooms) > 0:
            raise NoAvailabilityError("No hay disponibilidad para las fechas seleccionadas")
