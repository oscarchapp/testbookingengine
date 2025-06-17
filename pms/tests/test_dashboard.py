import pytest
from django.urls import reverse
from django.test import Client

from pms.models import Room , Booking


@pytest.mark.django_db
def test_dashboard_occupancy_percentage():
    client = Client()

    # Crear 5 habitaciones
    for i in range(5):
        Room.objects.create(name=f"Room {i+1}", room_type_id=1)

    # Crear 3 reservas confirmadas
    rooms = Room.objects.all()[:3]
    for i, room in enumerate(rooms):
        Booking.objects.create(
            state='NEW',
            checkin='2025-06-14',
            checkout='2025-06-16',
            room=room,
            guests=2,
            customer_id=1,  # ajusta si tienes otro modelo
            total=100.00,
            code=f"CODE{i+1}"
        )

    # Acceder al dashboard
    response = client.get(reverse('dashboard'))

    assert response.status_code == 200
    assert 'occupancy_percentage' in response.context['dashboard']

    # Comprobamos que el porcentaje sea 3/5 = 60%
    assert response.context['dashboard']['occupancy_percentage'] == 60.0
