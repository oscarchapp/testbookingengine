from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse, NoReverseMatch

from pms.forms import RoomFilterForm
from pms.models import Room, Room_type
from pms.views import RoomsView


class RoomViewTest(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        room_type = Room_type.objects.create(name="fake", price=50, max_guests=1)
        Room.objects.create(room_type=room_type, name="Room 1.1", description="fake")
        Room.objects.create(room_type=room_type, name="Room 2.1", description="fake")
        Room.objects.create(room_type=room_type, name="Room 2.2", description="fake")
        self.room_1_1 = model_to_dict(Room.objects.get(name="Room 1.1"))

    @staticmethod
    def __get_response_data(response) -> tuple:
        response_rooms = list(response.context['rooms'].values())
        return response_rooms, [r.get('id') for r in response_rooms]

    def test_filter_room_get_all_rooms(self):
        response = self.client.get(reverse('rooms'))
        response_rooms, response_rooms_ids = self.__get_response_data(response)
        self.assertTrue(self.room_1_1.get('id') in response_rooms_ids)
        self.assertEqual(len(response_rooms), 3)

    def test_filter_room_get_correct_rooms(self):
        response = self.client.get(reverse('rooms') + "?room_number=1")
        response_rooms, response_rooms_ids = self.__get_response_data(response)
        self.assertTrue(self.room_1_1.get('id') in response_rooms_ids)
        self.assertEqual(len(response_rooms), 2)

    def test_filter_room_get_correct_room(self):
        response = self.client.get(reverse('rooms') + "?room_number=2.1")
        response_rooms, response_rooms_ids = self.__get_response_data(response)
        self.assertTrue(self.room_1_1.get('id') not in response_rooms_ids)
        self.assertEqual(len(response_rooms), 1)

    def test_filter_room_get_no_rooms(self):
        response = self.client.get(reverse('rooms') + "?room_number=9")
        response_rooms, response_rooms_ids = self.__get_response_data(response)
        self.assertEqual(len(response_rooms), 0)

    def test_url_matches_correct_view(self):
        response = self.client.get(reverse('rooms'))
        expected_view = RoomsView
        self.assertEqual(response.resolver_match.func.view_class, expected_view)

    def test_url_no_matches_view(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fake-url'))

    def test_get_method_is_allowed(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)

    def test_post_method_is_not_allowed(self):
        response = self.client.post(reverse('rooms'))
        self.assertEqual(response.status_code, 405)

    """ TEMPLATE TEST """

    def test_correct_template_is_rendered(self):
        response = self.client.get(reverse('rooms') + '?room_number=1')
        self.assertTemplateUsed(response, 'rooms.html')

    def test_no_rooms_alert_is_load(self):
        response = self.client.get(reverse('rooms') + "?room_number=9")
        alert_text = "No existen habitaciones"  # TODO: improve codification of alert
        self.assertIn(alert_text, str(response.content))


class RoomFormTest(TestCase):
    def setUp(self) -> None:
        self.correct_room_number = 1.1
        self.wrong_room_number = "fake"

    def test_form_is_valid(self):
        form = RoomFilterForm({'room_number': self.correct_room_number})
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form = RoomFilterForm({'room_number': self.wrong_room_number})
        self.assertFalse(form.is_valid())

    def test_form_raise_validation_error(self):
        form = RoomFilterForm({'room_number': self.wrong_room_number})
        form.is_valid()
        self.assertIn("room_number", form.errors)
        self.assertIn("Room number provided is not a number.", form.errors['room_number'])

    def test_form_raise_field_required(self):
        form = RoomFilterForm({'room_number': ""})
        form.is_valid()
        self.assertIn("room_number", form.errors)
        self.assertIn("This field is required.", form.errors['room_number'])


class RoomModelTest(TestCase):

    def test_create_room_works(self):
        r = Room.objects.create(name='fake', description='fake')
        self.assertEqual(r.name, 'fake')
