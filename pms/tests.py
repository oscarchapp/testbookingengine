from django.test import TestCase, Client
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
            Booking(checkin="2023-09-01", checkout="2023-09-12", room=Room.objects.get(name="Room 1.1"), guests=1, customer=Customer.objects.get(name="Señor Test"), total=20, code="TEST1"),
            Booking(checkin="2024-10-04", checkout="2024-10-20", room=Room.objects.get(name="Room 2.1"), guests=2, customer=Customer.objects.get(name="Señor Test"), total=30, code="TEST2"),
            Booking(checkin="2023-02-01", checkout="2023-02-01", room=Room.objects.get(name="Room 3.1"), guests=3, customer=Customer.objects.get(name="Señor Test"), total=40, code="TEST3"),])
        
    def test_connection_room(self):
        client = Client()
        response = client.get("/rooms/")
        self.assertEqual(response.status_code, 200)
        
    def test_room_type_check(self):
        room_type = Room_type.objects.get(name="Single")
        self.assertEqual(room_type.name, "Single")
        self.assertEqual(room_type.price, 20) #cambiar a otro para que no pase el test
        self.assertEqual(room_type.max_guests, 1)
        
    def test_search_room(self):
        input_search = "Room 2.1"
        room = Room.objects.all().values("name")
        froom = room.filter(name__icontains=input_search)
        self.assertNotEqual(len(froom), 0, msg="Debe de haber al menos una habitación que coincida con la búsqueda")