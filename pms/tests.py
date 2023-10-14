from django.test import TestCase
from django.urls import reverse
from .models import Room, Room_type
from .forms import RoomFilterForm

class RoomsViewTest(TestCase):
    def setUp(self):
        self.room_type = Room_type.objects.create(name="Test Type", price=100, max_guests=2)
        self.room1 = Room.objects.create(room_type=self.room_type, name="Room 101", description="Room description")
        self.room2 = Room.objects.create(room_type=self.room_type, name="Room 102", description="Room description")
        
    def test_rooms_view_with_valid_filter(self):
        response = self.client.get(reverse('rooms'), {'search': 'Room 101'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 101 (Test Type)')
        self.assertNotContains(response, 'Room 102 (Test Type)')
        
    def test_rooms_view_with_invalid_filter(self):
        response = self.client.get(reverse('rooms'), {'search': 'Non-existent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Room 101 (Test Type)')
        self.assertNotContains(response, 'Room 102 (Test Type)')
        
    def test_rooms_view_with_empty_filter(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 101 (Test Type)')
        self.assertContains(response, 'Room 102 (Test Type)')
        
    def test_rooms_view_form_initial(self):
        response = self.client.get(reverse('rooms'))
        self.assertIsInstance(response.context['form'], RoomFilterForm)
        
    def test_rooms_view_template_used(self):
        response = self.client.get(reverse('rooms'))
        self.assertTemplateUsed(response, 'rooms.html')
