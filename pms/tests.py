from django.test import TestCase
from .models import Room

class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(name="Room 1",description="Room number 1")
        Room.objects.create(name="Room 1.2",description="Room number 1.2")
        Room.objects.create(name="Room 2",description="Room number 2")

    def test_get_by_name_correctly(self):
        room1 = Room.objects.get(name="Room 1")
        self.assertEqual(room1.description, "Room number 1")
        self.assertFalse(Room.objects.filter(name="NoExiste").exists())

    def test_get_by_description_correctly(self):
        room1 = Room.objects.get(description="Room number 1")
        self.assertEqual(room1.name, "Room 1")
        self.assertFalse(Room.objects.filter(description="NoExiste").exists())

    #test that represents the first requirement
    def test_filter_room_panel(self):
        rooms = Room.objects.filter(name__startswith="Room 1").values("name")
        self.assertIn({"name":"Room 1"},rooms)
        self.assertIn({"name":"Room 1.2"},rooms)
        self.assertNotIn({"name":"Room 2"},rooms)
    
