from django.test import RequestFactory, TestCase, SimpleTestCase
from django.urls import reverse, resolve

from pms.models import Room, Room_type
from pms.tests.MockData import MockData
from pms.views import RoomsView


class RoomsPageTest(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        MockData().startMockData()

    def test_matched_url_return_200(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)

    def test_method_not_allowed(self):
        response = self.client.post(reverse('rooms'))
        self.assertEqual(response.status_code, 405)

    def test_url_with_params_matched_correct_url(self):
        response = self.client.get(reverse('rooms') + '?filter=2.1')
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        response = self.client.get(reverse('rooms') + '?filter=2.1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms.html')

    def test_list_all_rooms_in_response(self):
        response = self.client.get(reverse('rooms'))
        self.assertGreater(response.context["rooms"].count(), 0)
        self.assertNotIn('NoResults', str(response.content))

    def test_list_rooms_by_filter_name_works(self):
        response = self.client.get(reverse('rooms') + '?filter=1.')
        self.assertEqual(response.context["rooms"].count(), 2)
        self.assertTrue(response.context["rooms"].filter(name__in=["1.1", "1.2"]).exists())

    def test_list_rooms_by_filter_name_no_return_value(self):
        response = self.client.get(reverse('rooms') + '?filter=fake')
        self.assertEqual(response.context["rooms"].count(), 0)
        self.assertIn('NoResults', str(response.content))
