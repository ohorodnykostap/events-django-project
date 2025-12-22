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

    def test_user_change_form_valid(self):
        user = User.objects.create_user(username="u", password="pass", email="a@b.com")
        form = CustomUserChangeForm(data={"first_name": "New", "last_name": "Name", "email": "new@example.com"}, instance=user)
        self.assertTrue(form.is_valid())

    def test_event_form_valid_future_date(self):
        future_datetime = timezone.now() + timezone.timedelta(days=5)
        data = {
            "name": "Test Event",
            "description": "Desc",
            "event_type": self.event_type.id,
            "location": self.location.id,
            "event_datetime": future_datetime,
            "price": 100,
            "capacity": 20,
        }
        form = EventForm(data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_past_date(self):
        past_datetime = timezone.now() - timezone.timedelta(days=5)
        data = {
            "name": "Past Event",
            "description": "Desc",
            "event_type": self.event_type.id,
            "location": self.location.id,
            "event_datetime": past_datetime,
            "price": 100,
            "capacity": 20,
        }
        form = EventForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("event_datetime", form.errors)
        self.assertEqual(
            form.errors["event_datetime"],
            ["You cannot create or edit an event in the past."]
        )



