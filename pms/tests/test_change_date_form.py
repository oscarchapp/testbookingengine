import pytest
from pms.forms import BookingDatesForm
from pms.tests.create_test_data import create_customer, create_room_type, create_room, create_reservation
from pms.models import Booking


@pytest.mark.django_db
def test_change_date_form_valid():
    # Given
    # Create customer
    customer = create_customer(
        name="Test Tester",
        email="test@test.com",
        phone="66666666"
    )
    # Create room type
    room_type = create_room_type(
        name="Single",
        max_guests=1,
        price=1000
    )
    # Create first room
    first_room = create_room(
        room_type=room_type,
        name="101"
    )
    # Set checkin and checkout
    checkin = "2020-01-01"
    checkout = "2020-01-02"
    # Create reservation
    reservation = create_reservation(
        room=first_room,
        checkin=checkin,
        checkout=checkout,
        guests=1,
        customer=customer
    )

    # When
    # Create second room
    second_room = create_room(
        room_type=room_type,
        name="102"
    )
    # Set form data
    form_data = {
        'checkin': checkin,
        'checkout': checkout,
    }
    # Test form
    form = BookingDatesForm(data=form_data, instance=reservation)

    # Then
    # Check form is valid
    assert form.is_valid()
    # Save form
    form.save()
    # Check if exist one reservation
    assert Booking.objects.count() == 1
    # Get reservation
    reservation = Booking.objects.get(room=second_room)
    # Check that new room is the second room
    assert reservation.room == second_room


@pytest.mark.django_db
def test_change_date_form_valid_not_exist_room():
    # Given
    # Create customer
    customer = create_customer(
        name="Test Tester",
        email="test@test.com",
        phone="66666666"
    )
    # Create room type
    room_type = create_room_type(
        name="Single",
        max_guests=1,
        price=1000
    )
    # Create first room
    first_room = create_room(
        room_type=room_type,
        name="101"
    )
    # Set checkin and checkout
    checkin = "2020-01-01"
    checkout = "2020-01-02"
    # Create reservation
    reservation = create_reservation(
        room=first_room,
        checkin=checkin,
        checkout=checkout,
        guests=1,
        customer=customer
    )

    # When
    # Set form data
    form_data = {
        'checkin': checkin,
        'checkout': checkout,
    }
    # Test form
    form = BookingDatesForm(data=form_data, instance=reservation)

    # Then
    # Check form is not valid
    assert not form.is_valid()
    # Check that form has error
    assert form.errors, f"Form has errors: {form.errors}"
    # Check that form has error in room
    assert form.errors['__all__'][0] == 'No hay habitaciones disponibles para las fechas seleccionadas.'
