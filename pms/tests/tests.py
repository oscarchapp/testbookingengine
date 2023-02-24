from django.test import TestCase

from datetime import datetime, timedelta

# Create your tests here.
from django.test import RequestFactory, TestCase, SimpleTestCase
from django.urls import reverse, resolve

from pms.models import Room, Room_type, Booking
from pms.reservation_code.generate import get
from pms.tests.MockDataTest import MockData
from pms.views import RoomsView


class RoomsPageTest(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        MockData().start_mock_data()

    def test_matched_url_return_200(self):
        response = self.client.get('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)

    def test_unmatched_url_return_404(self):
        response = self.client.get('/booking/1111/edit-dates')
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        response = self.client.put('/booking/1111/edit-dates')
        self.assertEqual(response.status_code, 405)

    def test_use_correct_template(self):
        response = self.client.get('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')
        self.assertIn((datetime.today() + timedelta(days=8)).strftime('%Y-%m-%d'), str(response.content))

    def test_method_post_allowed(self):
        response = self.client.post('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)

    def test_method_post_allowed_(self):
        response = self.client.post('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.post('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')

    def test_view_returns_cannot_save_action(self):
        d1 = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        d2 = (datetime.today() + timedelta(days=8)).strftime('%Y-%m-%d')
        query = {"booking_dates-checkin": d1, "booking_dates-checkout": d2}
        response = self.client.post('/booking/1/edit-dates', query)
        self.assertIn("No hay disponibilidad para las fechas seleccionadas", str(response.content))

    def test_view_returns_can_save_action(self):
        d1 = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        d2 = (datetime.today() + timedelta(days=8)).strftime('%Y-%m-%d')
        query = {"booking_dates-checkin": d1, "booking_dates-checkout": d2}
        response = self.client.post('/booking/2/edit-dates', query)
        self.assertEqual(response.status_code, 302)
