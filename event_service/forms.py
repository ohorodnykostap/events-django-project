from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import User, Event


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "role")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "event_type",
            "location",
            "event_datetime",
            "price",
            "capacity",
        ]
        widgets = {
            "event_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

    def clean_event_datetime(self):
        event_datetime = self.cleaned_data["event_datetime"]

        if event_datetime < timezone.now():
            raise forms.ValidationError(
                "You cannot create or edit an event in the past."
            )

        return event_datetime
