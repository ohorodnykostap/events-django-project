from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RegisterView,
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    ProfileView,
    BookingCreateView,
    BookingDeleteView,
    BookingCancelView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("events/create/", EventCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/update/", EventUpdateView.as_view(), name="event-update"),
    path("booking/<int:pk>/create/", BookingCreateView.as_view(), name="booking-create"),
    path("booking/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking-delete"),
    path("booking/<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

    path("login/",
         auth_views.LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(next_page="/"),
         name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    path("profile/", ProfileView.as_view(), name="profile"),
]