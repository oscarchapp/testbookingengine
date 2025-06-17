import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from ..models import Booking, Customer, Room

@pytest.mark.django_db
def test_editar_fechas_reserva_exitosa(client):
    # Crear habitación y cliente
    room = Room.objects.create(name="Room 101")
    customer = Customer.objects.create(name="Cliente Uno", email="uno@mail.com", phone="123456")

    # Reserva existente
    booking = Booking.objects.create(
        customer=customer,
        room=room,
        checkin=timezone.now().date() + timedelta(days=5),
        checkout=timezone.now().date() + timedelta(days=7),
        state='NEW',
        guests=2,
        total=100.0,
        code="ABC123"
    )

    # Nuevas fechas sin conflicto
    new_checkin = timezone.now().date() + timedelta(days=10)
    new_checkout = timezone.now().date() + timedelta(days=12)

    response = client.post(
        reverse('edit_booking_dates', args=[booking.id]),
        data={'checkin': new_checkin, 'checkout': new_checkout},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Indica que es una solicitud AJAX
    )

    assert response.status_code == 200
    json = response.json()
    assert json['success'] is True
    assert json['message'] == 'Reserva actualizada correctamente'

    # Verificar cambio en la base de datos
    booking.refresh_from_db()
    assert booking.checkin == new_checkin
    assert booking.checkout == new_checkout


@pytest.mark.django_db
def test_editar_fechas_reserva_conflicto(client):
    # Crear habitación y cliente
    room = Room.objects.create(name="Room 102")
    customer1 = Customer.objects.create(name="Cliente Uno", email="uno@mail.com", phone="123456")
    customer2 = Customer.objects.create(name="Cliente Dos", email="dos@mail.com", phone="654321")

    # Reserva existente en el rango conflictivo
    Booking.objects.create(
        customer=customer1,
        room=room,
        checkin=timezone.now().date() + timedelta(days=10),
        checkout=timezone.now().date() + timedelta(days=12),
        state='NEW',
        guests=2,
        total=150.0,
        code="CONFLICT"
    )

    # Otra reserva que vamos a intentar editar a fechas que se superponen
    booking_to_edit = Booking.objects.create(
        customer=customer2,
        room=room,
        checkin=timezone.now().date() + timedelta(days=13),
        checkout=timezone.now().date() + timedelta(days=14),
        state='NEW',
        guests=1,
        total=80.0,
        code="EDITME"
    )

    # Intentamos poner fechas en conflicto
    conflict_checkin = timezone.now().date() + timedelta(days=11)
    conflict_checkout = timezone.now().date() + timedelta(days=13)

    response = client.post(
        reverse('edit_booking_dates', args=[booking_to_edit.id]),
        data={'checkin': conflict_checkin, 'checkout': conflict_checkout},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )

    assert response.status_code == 200
    json = response.json()
    assert json['success'] is False
    assert json['message'] == 'No hay disponibilidad para las fechas seleccionadas'

    # Asegurar que no se actualizaron
    booking_to_edit.refresh_from_db()
    assert booking_to_edit.checkin != conflict_checkin