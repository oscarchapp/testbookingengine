import pytest
from pms.forms import get_first_equal_room_available
from pms.tests.create_test_data import create_customer, create_room_type, create_room, create_reservation
from pms.form_dates import Ymd


@pytest.mark.django_db
def test_get_new_room():
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
    create_reservation(
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
    # Get new room
    new_room = get_first_equal_room_available(
        checkin=checkin,
        checkout=checkout,
        room_type=room_type
    )

    # Then
    # Check that new room is the second room
    assert new_room == second_room


@pytest.mark.django_db
def test_get_new_room_not_exist_room():
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
    create_reservation(
        room=first_room,
        checkin=checkin,
        checkout=checkout,
        guests=1,
        customer=customer
    )

    # When
    # Get new room
    new_room = get_first_equal_room_available(
        checkin=checkin,
        checkout=checkout,
        room_type=room_type
    )

    # Then
    # Check that new room is the second room
    assert not new_room
