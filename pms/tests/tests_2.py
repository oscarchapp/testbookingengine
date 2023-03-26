from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse, NoReverseMatch

from pms.models import Room, Room_type, Booking
from pms.views import DashboardView


class DashboardViewTest(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        room_type = Room_type.objects.create(name="fake", price=50, max_guests=1)
        room_1_1 = Room.objects.create(room_type=room_type, name="Room 1.1", description="fake")
        room_2_1 = Room.objects.create(room_type=room_type, name="Room 2.1", description="fake")
        room_2_2 = Room.objects.create(room_type=room_type, name="Room 2.2", description="fake")
        room_3_2 = Room.objects.create(room_type=room_type, name="Room 3.2", description="fake")

        b_1 = Booking.objects.create(room=room_1_1, checkin=date.today() - timedelta(days=5),
                                     checkout=date.today() - timedelta(days=3), guests=1)  # 2 days / total = 100
        b_2 = Booking.objects.create(room=room_2_1, checkin=date.today() - timedelta(days=1),
                                     checkout=date.today() + timedelta(days=3), guests=1)  # 4 days / total = 200 / book
        b_3 = Booking.objects.create(room=room_2_2, checkin=date.today(), checkout=date.today() + timedelta(days=5),
                                     guests=1)  # 5 days / total = 250 / booked
        b_4 = Booking.objects.create(room=room_3_2, checkin=date.today() + timedelta(days=2),
                                     checkout=date.today() + timedelta(days=5), guests=1)  # 3 days / total = 150
        b_5 = Booking.objects.create(room=room_1_1, checkin=date.today() - timedelta(days=2), checkout=date.today(),
                                     guests=1)  # 2 days / total = 100
        b_6 = Booking.objects.create(room=room_1_1, checkin=date.today() - timedelta(days=2), checkout=date.today(),
                                     guests=1, state="DEL")  # 2 days / total = 100

        self.context_result = {
            'new_bookings': 6,
            'incoming_guests': 1,  # b_3
            'outcoming_guests': 1,  # b_5
            'invoiced': 800,  # 100 + 200 + 250 + 150 + 100
            'percentage': 50  # booked_rooms(2) / total_rooms(4) * 100
        }

    def test_get_method_is_allowed(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_post_method_is_not_allowed(self):
        response = self.client.post(reverse('dashboard'))
        self.assertEqual(response.status_code, 405)

    def test_url_matches_correct_view(self):
        response = self.client.get(reverse('dashboard'))
        expected_view = DashboardView
        self.assertEqual(response.resolver_match.func.view_class, expected_view)

    def test_url_no_matches_view(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fake-url'))

    def test_view_context_data(self):

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context["dashboard"].get("new_bookings"), self.context_result.get("new_bookings"))
        self.assertEqual(response.context["dashboard"].get("incoming_guests"),
                         self.context_result.get("incoming_guests"))
        self.assertEqual(response.context["dashboard"].get("outcoming_guests"),
                         self.context_result.get("outcoming_guests"))
        self.assertEqual(response.context["dashboard"].get("invoiced").get("total__sum"),
                         self.context_result.get("invoiced"))
        self.assertEqual(response.context["dashboard"].get("percentage"), self.context_result.get("percentage"))

    def test_view_avoid_zerodivisionerror(self):
        Room.objects.all().delete()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context["dashboard"].get("new_bookings"), self.context_result.get("new_bookings"))
        self.assertEqual(response.context["dashboard"].get("incoming_guests"),
                         self.context_result.get("incoming_guests"))
        self.assertEqual(response.context["dashboard"].get("outcoming_guests"),
                         self.context_result.get("outcoming_guests"))
        self.assertEqual(response.context["dashboard"].get("invoiced").get("total__sum"),
                         self.context_result.get("invoiced"))
        self.assertEqual(response.context["dashboard"].get("percentage"), 0)

    """ TEMPLATE TEST """

    def test_correct_template_is_rendered(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_built_in_filter_works(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn("50.0", str(response.content))
