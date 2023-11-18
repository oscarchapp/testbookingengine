from django.test import TestCase, override_settings
from django.urls import reverse
from pms.tests.factory import RoomFactory

_SFS ='django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=_SFS)
class RoomViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room_names = ["Room 1.1", "Room 1.12", "Room 1.2"]
        for room_name in cls.room_names:
            RoomFactory.create(name=room_name)

    def test_get_all_rooms(self):
        """
        This test check that the endpoint returns a list of all the
        rooms in database rendered in html
        """
        response = self.client.get(reverse('rooms'))
        rooms_qs = response.context.get("rooms")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(rooms_qs.values_list("name", flat=True), self.room_names)


    def test_get_filtered_rooms(self):
        """
        This test check that the endpoint returns a filtered list of all the
        rooms in database rendered in html
        """
        response = self.client.get(reverse('rooms'), {"room_name": "Room 1.1"})
        rooms_qs = response.context.get("rooms")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rooms_qs.count(), 2)

    def test_dont_return_any_rooms(self):
        """
        This test check that the endpoint returns an empty list of rooms
        and display a descriptive messaje rendered in html
        """
        response = self.client.get(reverse('rooms'), {"room_name": "Invalid name"})
        rooms_qs = response.context.get("rooms")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rooms_qs.count(), 0)
        self.assertContains(response, 'No hay resultados')
