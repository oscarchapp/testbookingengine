from django.db import models, transaction

from .models import Booking

class BookingManager(models.Manager):

    def update_booking_dates(self, booking, checkin, checkout):

        try:
            with transaction.atomic():
                booking.checkin = checkin.date
                booking.checkout = checkout.date
                booking.save()
        except Exception as e:
            raise e
