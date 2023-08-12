from pms.models import Customer, Room, Room_type, Booking
from pms.form_dates import Ymd
from pms.reservation_code import generate


def create_customer(name, email, phone):
    """Create a customer"""
    customer = Customer()
    customer.name = name
    customer.email = email
    customer.phone = phone
    customer.save()
    return customer


def create_room_type(name, max_guests, price):
    """Create a room type"""
    room_type = Room_type()
    room_type.name = name
    room_type.max_guests = max_guests
    room_type.price = price
    room_type.save()
    return room_type


def create_room(room_type, name):
    """Create a room"""
    room = Room()
    room.room_type = room_type
    room.name = name
    room.save()
    return room

def create_reservation(room, checkin, checkout, guests, customer):
    """Create a reservation"""
    reservation = Booking()
    reservation.room = room
    reservation.checkin = checkin
    reservation.checkout = checkout
    reservation.guests = guests
    reservation.customer = customer
    reservation.total = (Ymd.Ymd(checkout) - Ymd.Ymd(checkin)) * room.room_type.price
    reservation.code = generate.get()
    reservation.save()
    return reservation
