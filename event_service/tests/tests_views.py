from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from event_service.models import Event, EventType, Location, Booking


User = get_user_model()


class EventViewsTestCase(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="org",
            email="org@test.com",
            password="pass1234",
            role="organizer"
        )

        self.participant = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="pass1234",
            role="participant"
        )

        self.event_type = EventType.objects.create(name="Concert")
        self.location = Location.objects.create(
            name="Arena",
            address="Lviv"
        )

        self.event = Event.objects.create(
            name="Test Event",
            description="Test description",
            event_datetime=timezone.now() + timezone.timedelta(days=10),
            price=100,
            capacity=10,
            organizer=self.organizer,
            event_type=self.event_type,
            location=self.location
        )

    def test_event_list_view(self):
        url = reverse("events:event-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.name)

    def test_event_detail_view(self):
        url = reverse("events:event-detail", args=[self.event.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.name)