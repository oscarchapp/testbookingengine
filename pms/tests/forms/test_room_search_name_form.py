from django.test import TestCase
from pms.forms import RoomSearchNameForm


class RoomSearchNameFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'My Room Name'
        }
        form = RoomSearchNameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_invalid_form(self):
        form_data = {
            'name': ''
        }
        form = RoomSearchNameForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_with_spaces(self):
        form_data = {
            'name': '  Name  '
        }
        form = RoomSearchNameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Name")
