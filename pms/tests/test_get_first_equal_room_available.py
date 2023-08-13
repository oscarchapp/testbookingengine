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
    # Get new room
    new_room = get_first_equal_room_available(
        checkin=checkin,
        checkout=checkout,
        original_room=reservation.room
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
    reservation = create_reservation(
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
        original_room=reservation.room
    )

    # Then
    # Check that new room is the second room
    assert not new_room


@pytest.mark.django_db
def test_get_room_in_other_dates():
    # Given
    # Create customer
    customer_one = create_customer(
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
    checkin_one = "2020-01-01"
    checkout_one = "2020-01-02"
    # Create first reservation
    reservation = create_reservation(
        room=first_room,
        checkin=checkin_one,
        checkout=checkout_one,
        guests=1,
        customer=customer_one
    )

    # When
    # Set checkin and checkout second reservation
    checkin_two = "2020-01-03"
    checkout_two = "2020-01-04"
    # Create second room
    second_room = create_room(
        room_type=room_type,
        name="102"
    )
    # Get original room
    original_room = get_first_equal_room_available(
        checkin=checkin_two,
        checkout=checkout_two,
        original_room=reservation.room
    )

    # Then
    # Check that new room is the second room
    assert original_room != second_room
    # Check that new room is the first room
    assert original_room == first_room


@pytest.mark.django_db
def test_get_new_room_in_other_dates():
    # Given
    # Create customer
    customer_one = create_customer(
        name="Test Tester",
        email="test@test.com",
        phone="66666666"
    )
    customer_two = create_customer(
        name="Test2 Tester2",
        email="test2@test.com",
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
    checkin_one = "2020-01-01"
    checkout_one = "2020-01-02"
    # Create first reservation
    customer_one_reservation = create_reservation(
        room=first_room,
        checkin=checkin_one,
        checkout=checkout_one,
        guests=1,
        customer=customer_one
    )
    # Set checkin and checkout second reservation
    checkin_two = "2020-01-03"
    checkout_two = "2020-01-04"
    # Create reservation
    create_reservation(
        room=first_room,
        checkin=checkin_two,
        checkout=checkout_two,
        guests=1,
        customer=customer_two
    )

    # When
    # Create second room
    second_room = create_room(
        room_type=room_type,
        name="102"
    )
    # Get new room
    new_room = get_first_equal_room_available(
        checkin=checkin_two,
        checkout=checkout_two,
        original_room=customer_one_reservation.room
    )

    # Then
    # Check that new room is the second room
    assert new_room == second_room
