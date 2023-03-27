from enum import Enum


class RoomFilterError:
    CODE = 1
    MESSAGE = "Room number provided is not a number."


class BookingEditDateError:
    CODE = 2
    MESSAGE = "Checkin date must be before checkout date."
