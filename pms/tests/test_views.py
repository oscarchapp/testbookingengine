from django.test import TestCase, Client
from django.urls import reverse
from pms.models import Room, Room_type


class RoomSearchViewTest(TestCase):
    client = Client()

    def setUp(self):
        self.url = reverse("rooms")
        self.room_type_simple = Room_type.objects.create(
            name="Simple", price=20, max_guests=2
        )
        self.room_type_double = Room_type.objects.create(
            name="Doble", price=30, max_guests=2
        )
        self.room_type_triple = Room_type.objects.create(
            name="Triple", price=40, max_guests=3
        )
        self.room_type_quadruple = Room_type.objects.create(
            name="Cuadruple", price=60, max_guests=6
        )
        self.room_1 = Room.objects.create(
            name="Room 1.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_2 = Room.objects.create(
            name="Room 2.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_3 = Room.objects.create(
            name="Room 3.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_3_2 = Room.objects.create(
            name="Room 3.2",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_4 = Room.objects.create(
            name="Room 4.1",
            description="Room 1",
            room_type=self.room_type_simple,
        )
        self.room_4 = Room.objects.create(
            name="Room 4.2",
            description="Room 1",
            room_type=self.room_type_simple,
        )

    def test_search_with_value_and_return_content(self):
        """
        Test to verify if the search works well
        """
        response = self.client.get(self.url, {"search": "1.1"})
        queryset = (
            Room.objects.filter(id=self.room_1.id)
            .values("name", "room_type__name", "id")
            .order_by("name")
        )
        context = response.context
        self.assertQuerysetEqual(context["rooms"].qs, queryset)

    def test_search_with_value_and_return_empty_content(self):
        response = self.client.get(self.url, {"search": "1.133"})
        context = response.context
        self.assertQuerysetEqual(context["rooms"].qs, [])

    def test_search_with_empty_value_and_return_empty_content(self):
        response = self.client.get(self.url, {"search": ""})
        context = response.context
        queryset = (
            Room.objects.all()
            .select_related("room_type")
            .values("name", "room_type__name", "id")
            .order_by("name")
        )
        self.assertQuerysetEqual(context["rooms"].qs, queryset)
