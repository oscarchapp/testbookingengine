# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from pms.tests.mockData import MockData
from pms.models import Booking


class RoomsPageTest(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        MockData().start_mock_data_for_test()

    def test_matched_url_return_200(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_unmatched_url_return_404(self):
        response = self.client.get('dashboard/fake')
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        response = self.client.post(reverse('dashboard'))
        self.assertEqual(response.status_code, 405)

    def test_use_correct_template(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_correct_type_data(self):
        response = self.client.get(reverse('dashboard'))
        context_template = response.context["dashboard"]
        self.assertIsInstance(context_template.get("new_bookings"), int)
        self.assertIsInstance(context_template.get("incoming_guests"), int)
        self.assertIsInstance(context_template.get("outcoming_guests"), int)
        self.assertIsInstance(context_template.get("invoiced"), dict)
        self.assertIsInstance(context_template.get("occupancy"), float)

    def test_get_correct_values_even_today_updates(self):
        Booking.objects.filter(id=1).update(state=Booking.DELETED)
        response = self.client.get(reverse('dashboard'))
        context_template = response.context["dashboard"]
        self.assertEqual(context_template.get("new_bookings"), 5)
        self.assertEqual(context_template.get("incoming_guests"), 2)
        self.assertEqual(context_template.get("outcoming_guests"), 0)
        self.assertEqual(context_template.get("occupancy"), 50.0)

    def test_get_correct_values_in_context(self):
        response = self.client.get(reverse('dashboard'))
        context_template = response.context["dashboard"]
        self.assertEqual(context_template.get("new_bookings"), 5)
        self.assertEqual(context_template.get("incoming_guests"), 3)
        self.assertEqual(context_template.get("outcoming_guests"), 0)
        self.assertEqual(context_template.get("invoiced").get("total__sum"), 100.0)
        self.assertEqual(context_template.get("occupancy"), 75.0)
