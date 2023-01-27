from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Room_type, Customer, Booking
# Create your tests here.


class TestPMS(TestCase):
    def setUp(self):
        self.create_room_type = Room_type.objects.bulk_create([
            Room_type(name="Single", price=20, max_guests=1),
            Room_type(name="Double", price=30, max_guests=2),
            Room_type(name="Triple", price=40, max_guests=3),
            Room_type(name="Quadruple", price=50, max_guests=4)])
        self.create_room = Room.objects.bulk_create([
            Room(room_type=Room_type.objects.get(name="Single"), name="Room 1.1", description="Single room"),
            Room(room_type=Room_type.objects.get(name="Single"), name="Room 1.2", description="Single room"),
            Room(room_type=Room_type.objects.get(name="Double"), name="Room 2.1", description="Double room"),
            Room(room_type=Room_type.objects.get(name="Double"), name="Room 2.2", description="Double room"),
            Room(room_type=Room_type.objects.get(name="Triple"), name="Room 3.1", description="Triple room"),
            Room(room_type=Room_type.objects.get(name="Quadruple"), name="Room 4.1", description="Quadruple room")])
        self.create_customer = Customer.objects.bulk_create([
            Customer(name="Señor Test", email="test@test.com", phone="565741222")])
        self.create_booking = Booking.objects.bulk_create([
            Booking(checkin="2023-01-26", checkout="2023-01-27", room=Room.objects.get(name="Room 1.1"), guests=1, customer=Customer.objects.get(name="Señor Test"), total=20, code="TEST1"),
            Booking(checkin="2023-01-26", checkout="2023-01-27", room=Room.objects.get(name="Room 1.2"), guests=2, customer=Customer.objects.get(name="Señor Test"), total=30, code="TEST2"),
            Booking(checkin="2023-01-26", checkout="2023-01-27", room=Room.objects.get(name="Room 2.1"), guests=3, customer=Customer.objects.get(name="Señor Test"), total=40, code="TEST3"),
            Booking(checkin="2023-01-26", checkout="2023-01-27", room=Room.objects.get(name="Room 2.2"), guests=1, customer=Customer.objects.get(name="Señor Test"), total=20, code="TEST1"),
            Booking(checkin="2023-02-02", checkout="2023-02-06", room=Room.objects.get(name="Room 4.1"), guests=2, customer=Customer.objects.get(name="Señor Test"), total=30, code="TEST2"),
            Booking(checkin="2023-02-03", checkout="2023-02-04", room=Room.objects.get(name="Room 4.1"), guests=3, customer=Customer.objects.get(name="Señor Test"), total=40, code="TEST3"),])
        
 
    def test_search_room(self):
        input_search = "Room 2.1"
        room = Room.objects.all().values("name")
        froom = room.filter(name__icontains=input_search)
        self.assertNotEqual(len(froom), 0, msg="Debe de haber al menos una habitación que coincida con la búsqueda")
        
    def test_occupacy_percen_room(self):
        from datetime import date
        today = date.today()
        room_ocupacy = (Booking.objects
                          .filter(checkin__lte=today, checkout__gte=today)
                          .exclude(state="DEL")
                          ).count() / Room.objects.all().count() * 100
        self.assertLess(room_ocupacy, 100, msg="El porcentaje de ocupación no puede ser mayor o igual que el 100%")
        
    def test_check_room_availability(self):
        room_availability = (Booking.objects
                             .filter(room=Room.objects.get(name=self.create_room[5].name),checkin__lte="2023-03-09", checkout__gte="2023-03-02", state="NEW")
                             .count())
        self.assertEqual(room_availability, 0, msg="No hay habitaciones disponibles")
        
    def test_post_edit_date_booking(self):
        c = Client()
        response = c.post(reverse('edit_booking_date', kwargs={'pk': self.create_booking[5].id}), {'booking-checkin': '2023-03-10', 'booking-checkout': '2023-03-11'}, follow=True)
        self.assertRedirects(response, reverse('home'), msg_prefix="No se ha podido editar la fecha de la reserva")
    