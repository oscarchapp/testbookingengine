from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from pms.models import Room, Booking

# Create your tests here.
class TestOccupancyPercentage(TestCase):
    def setUp(self):
        # Create rooms
        self.room1 = Room.objects.create(name='Habitación 1', room_type=None, description='Habitación estándar')
        self.room2 = Room.objects.create(name='Habitación 2', room_type=None, description='Habitación estándar')
        self.room3 = Room.objects.create(name='Habitación 3', room_type=None, description='Habitación estándar')        

        # Create reservations
        self.booking1 = Booking.objects.create(
            state='NEW', checkin='2022-01-01', checkout='2022-01-05',
            room=self.room1, guests=2, customer=None, total=100, code='ABCDEFGH'
        )
        self.booking2 = Booking.objects.create(
            state='NEW', checkin='2022-01-02', checkout='2022-01-07',
            room=self.room2, guests=2, customer=None, total=200, code='IJKLMNOP'
        )
        self.booking3 = Booking.objects.create(
            state='DEL', checkin='2022-01-03', checkout='2022-01-08',
            room=self.room3, guests=2, customer=None, total=300, code='QRSTUVWX'
        )

    # Test to check that the % occupancy widget is displayed on the dashboard:
    def test_occupancy_widget_displayed(self):
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, '% Ocupación')

    # Test to check that the % occupancy calculation is correct:
    def test_occupancy_percentage_calculation(self):
        # Obtain the total number of rooms
        total_rooms = Room.objects.count()
        # Get the number of confirmed reservations
        confirmed_bookings = Booking.objects.filter(state='NEW').count()
        # calculates the percentage to test
        test_percentage = confirmed_bookings / total_rooms * 100

        # now compared to the percentage shown in the application:
        response = self.client.get('/dashboard/')
        real_percentage = response.context.get('dashboard').get('occupation_percentage')

        # Check that the calculation is correct
        self.assertEqual(test_percentage, real_percentage)