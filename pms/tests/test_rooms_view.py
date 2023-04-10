from django.test import TestCase
from django.urls import reverse, resolve

from pms.models import Room, Room_type
from pms.views import RoomsView


class RoomsViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room_type = Room_type.objects.create(name="Single", price=20.00, max_guests=1)
        cls.room_1 = Room.objects.create(name="Room 1", room_type=cls.room_type)
        cls.room_2 = Room.objects.create(name="Room 2", room_type=cls.room_type)

    def test_rooms_resolves(self):
        url = reverse("rooms")
        view_class = resolve(url).func.view_class
        self.assertEqual(view_class, RoomsView)

    def test_status_code(self):
        response = self.client.get(reverse("rooms"))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(reverse("rooms"))
        self.assertTemplateUsed(response, "rooms.html")

    def test_room_list(self):
        rooms = Room.objects.all().values("name", "room_type__name", "id")
        response = self.client.get(reverse("rooms"))
        self.assertListEqual(list(response.context["rooms"]), list(rooms))

    def test_room_filter(self):
        room_1 = Room.objects.filter(pk=self.room_1.id).values("name", "room_type__name", "id")
        response = self.client.get(reverse("rooms"), {"room_name": "Room 1"})
        self.assertListEqual(list(response.context["rooms"]), list(room_1))

    def test_room_filter_missing_name(self):
        all_rooms = Room.objects.all().values("name", "room_type__name", "id")
        response = self.client.get(reverse("rooms"), {"room_name": "  "})
        self.assertListEqual(list(response.context["rooms"]), list(all_rooms))

    def test_room_filter_no_match(self):
        response = self.client.get(reverse("rooms"), {"room_name": "Room 6543"})
        self.assertListEqual(list(response.context["rooms"]), [])
