from datetime import date

from django.test import TestCase
from django.urls import reverse, NoReverseMatch

from pms.forms import BookingDateForm
from pms.models import Room, Room_type, Booking
from pms.utils.custom_errors import BookingEditDateError
from pms.views import EditBookingDateView


class BookingDateFormTest(TestCase):
    def setUp(self) -> None:
        self.correct_dates = {'checkin': date(2023, 3, 2), 'checkout': date(2023, 3, 4)}
        self.wrong_dates = {'checkin': date(2023, 3, 2), 'checkout': date(2023, 3, 1)}

    def test_form_is_valid(self):
        form = BookingDateForm(self.correct_dates)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form = BookingDateForm(self.wrong_dates)
        self.assertFalse(form.is_valid())

    def test_form_raise_validation_error(self):
        form = BookingDateForm(self.wrong_dates)
        form.is_valid()
        self.assertIn("__all__", form.errors)
        self.assertIn(BookingEditDateError.MESSAGE, form.errors["__all__"])


class EditBookingDateViewTestGetMethod(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        room_type = Room_type.objects.create(name="fake", price=50, max_guests=1)
        room_1_1 = Room.objects.create(room_type=room_type, name="Room 1.1", description="fake")

        base_booking_fields = {'guests': 1, 'room': room_1_1}
        ref_dates = {'checkin': date(2023, 3, 3), 'checkout': date(2023, 3, 5), 'code': "ref_dates"}

        self.booking_ref = Booking.objects.create(**base_booking_fields, **ref_dates)

    def test_get_method_is_allowed(self):
        response = self.client.get('/booking/1/edit-dates')
        self.assertEqual(response.status_code, 200)

    def test_get_method_return_404(self):
        response = self.client.get('/booking/191919191/edit-dates')
        self.assertEqual(response.status_code, 404)

    def test_url_matches_correct_view(self):
        response = self.client.get('/booking/1/edit-dates')
        expected_view = EditBookingDateView
        self.assertEqual(response.resolver_match.func.view_class, expected_view)

    def test_url_no_matches_view(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fake-url'))

    """ TEMPLATE TEST """

    def test_correct_template_is_rendered(self):
        response = self.client.get('/booking/1/edit-dates')
        self.assertTemplateUsed(response, 'edit_booking_dates.html')

    def test_built_in_filter_works(self):
        response = self.client.get('/booking/1/edit-dates')
        self.assertIn(str(self.booking_ref.checkin), str(response.content))


class EditBookingDateViewTestPostMethod(TestCase):
    databases = '__all__'

    def setUp(self) -> None:
        room_type = Room_type.objects.create(name="fake", price=50, max_guests=1)
        room_1_1 = Room.objects.create(room_type=room_type, name="Room 1.1", description="fake")

        base_booking_fields = {'guests': 1, 'room': room_1_1}
        self.old_dates = {'checkin': date(2023, 3, 3), 'checkout': date(2023, 3, 5), 'code': "booking_2_edit"}
        self.ref_dates = {'checkin': date(2023, 3, 5), 'checkout': date(2023, 3, 9), 'code': "booking_ref"}
        self.date_with_overlap = {'checkin': date(2023, 3, 2), 'checkout': date(2023, 3, 6), 'code': "overlap"}
        self.date_without_overlap = {'checkin': date(2023, 3, 20), 'checkout': date(2023, 3, 22), 'code': "no_overlap"}

        self.booking_2_edit = Booking.objects.create(**base_booking_fields, **self.old_dates)  # id=1
        self.booking_ref = Booking.objects.create(**base_booking_fields, **self.ref_dates)

    def test_cannot_edit_booking_get_200_code(self):
        response = self.client.post('/booking/1/edit-dates', data=self.date_with_overlap)
        self.assertEqual(response.status_code, 200)

    def test_edit_booking_success_get_302_code(self):
        response = self.client.post('/booking/1/edit-dates', data=self.date_without_overlap)
        self.assertEqual(response.status_code, 302)

    def test_url_matches_correct_view(self):
        response = self.client.post('/booking/1/edit-dates',  data=self.ref_dates)
        expected_view = EditBookingDateView
        self.assertEqual(response.resolver_match.func.view_class, expected_view)

    def test_check_overlapping_exists(self):
        response = self.client.post('/booking/1/edit-dates', data=self.date_with_overlap)
        self.assertIn("No hay disponibilidad para las fechas seleccionadas.", str(response.content))

    def test_check_overlapping_no_exists(self):
        response = self.client.post('/booking/1/edit-dates', data=self.date_without_overlap)
        self.assertNotIn("No hay disponibilidad para las fechas seleccionadas.", str(response.content))

    """ TEMPLATE TEST """

    def test_correct_template_is_rendered(self):
        response = self.client.post('/booking/1/edit-dates', data=self.ref_dates)
        self.assertTemplateUsed(response, 'edit_booking_dates.html')
