from django.test import TestCase, Client
from .models import Room, Room_type

class RoomTestCase(TestCase):

    client = Client()

    def setUp(self):
        self.roomtype_simple = Room_type.objects.create(name = "Simple",price = 20,max_guests = 1)
        self.roomtype_doble = Room_type.objects.create(name = "Doble",price = 30,max_guests = 2)
        self.roomtype_triple = Room_type.objects.create(name = "Triple",price = 40,max_guests = 3)
        self.roomtype_cuadruple = Room_type.objects.create(name = "Cuadruple",price = 50,max_guests = 4)

        self.room_simple = Room.objects.create(room_type = self.roomtype_simple,name = "Room 1.1",description = "Testing room simple")
        self.room_doble = Room.objects.create(room_type = self.roomtype_doble,name = "Room 2.1",description = "Testing room doble")
        self.room_triple = Room.objects.create(room_type = self.roomtype_triple,name = "Room 3.1",description = "Testing room triple")
        self.room_cuadruple = Room.objects.create(room_type = self.roomtype_cuadruple,name = "Room 4.1",description = "Testing room cuadruple")
    
    def test_search_room(self):
        """test search room"""
        response = self.client.post('/search/room/',{'checkin': '2022-11-06', 'checkout': '2022-11-07', 'guests': '1'} )
        self.assertEqual(response.status_code, 200)

    def test_room_cuadruple(self):
        """test 4 guests """
        response = self.client.post('/search/room/',{'checkin': '2022-11-06', 'checkout': '2022-11-07', 'guests': '4'} )
        self.assertQuerysetEqual(response.context['rooms'],[self.room_cuadruple])

    def test_room_doble(self):
        """test 2 guests """
        response = self.client.post('/search/room/',{'checkin': '2022-11-06', 'checkout': '2022-11-07', 'guests': '2'} )
        self.assertQuerysetEqual(response.context['rooms'],[self.room_doble,self.room_triple,self.room_cuadruple])

    

