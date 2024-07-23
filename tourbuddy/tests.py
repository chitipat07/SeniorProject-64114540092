from django.test import TestCase

# Create your tests here.
# tests.py

from django.test import TestCase
from django.urls import reverse
from .models import TouristNode

class NottiViewTest(TestCase):
    def test_notti_view_with_tourist_node_exists(self):
        # Create a TouristNode instance for testing
        TouristNode.objects.create(name='Test Node', location='Test Location')

        # Access the view Notti
        response = self.client.get(reverse('Notti'))

        # Check if the view returns a JSON response with tourist_node_exists as True
        self.assertJSONEqual(response.content, {'tourist_node_exists': True})

    def test_notti_view_without_tourist_node_exists(self):
        # Access the view Notti
        response = self.client.get(reverse('Notti'))

        # Check if the view returns a JSON response with tourist_node_exists as False
        self.assertJSONEqual(response.content, {'tourist_node_exists': False})
