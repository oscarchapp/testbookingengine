from django.test import TestCase, Client

from .models import Room, Room_type


# Create your tests here.
class TestRoomFilter(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

        test_room_type = Room_type.objects.create(
            name="test",
            price=10,
            max_guests=2
        )
        Room.objects.create(
            room_type=test_room_type,
            name="room 1.1",
            description="test room"
        )
        Room.objects.create(
            room_type=test_room_type,
            name="room 1.2",
            description="test room"
        )
        Room.objects.create(
            room_type=test_room_type,
            name="room 2.1",
            description="test room"
        )

    
    def test_filter_rooms(self) -> None:
        response = self.client.get("/rooms/?filter=room 1")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "room 2.1")