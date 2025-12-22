from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ("organizer", "Organizer"),
        ("participant", "Participant"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="participant",
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("events:user-detail", kwargs={"pk": self.pk})


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_PLANNED = "planned"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_COMPLETED, "Completed"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PLANNED,
    )

    organizer = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.PROTECT,
        related_name="events",
    )
    event_type = models.ForeignKey(
        "EventType",
        on_delete=models.PROTECT,
        related_name="events",
    )

    class Meta:
        ordering = ["event_datetime"]

    def __str__(self):
        return f"{self.name} ({self.event_datetime.date()})"

    def get_absolute_url(self):
        return reverse("events:event-detail", kwargs={"pk": self.pk})

    @property
    def is_completed(self):
        return self.event_datetime < timezone.now()

    def update_status(self):
        if self.is_completed and self.status == self.STATUS_PLANNED:
            self.status = self.STATUS_COMPLETED
            self.save(update_fields=["status"])

    def available_seats(self):
        booked = Booking.objects.filter(event=self).count()
        return self.capacity - booked


class Booking(models.Model):
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CONFIRMED,
    )

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user} → {self.event}"
