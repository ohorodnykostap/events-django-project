from django.test import TestCase
from django.utils import timezone
from event_service.forms import CustomUserCreationForm, CustomUserChangeForm, EventForm
from event_service.models import User, EventType, Location

class FormsTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "role": "participant"
        }

        self.event_type = EventType.objects.create(name="Concert")
        self.location = Location.objects.create(name="Arena", address="Lviv")

    def test_user_creation_form_valid(self):
        form = CustomUserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_missing_first_name(self):
        data = self.user_data.copy()
        data.pop("first_name")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

