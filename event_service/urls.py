from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RegisterView,
    EventListView,
    EventDetailView,
    booking_create,
    ProfileView,
    EventCreateView,
    EventUpdateView,
    cancel_booking,
    booking_delete,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("<int:pk>/booking/", booking_create, name="booking-create"),

    path("login/",
         auth_views.LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(next_page="/"),
         name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path("events/create/", EventCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/update/",
         EventUpdateView.as_view(),
         name="event-update"),

    path("booking/<int:pk>/cancel/", cancel_booking, name="cancel-booking"),
    path("booking/<int:pk>/delete/", booking_delete, name="booking-delete"),
    path("events/create/", EventCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/update/",
         EventUpdateView.as_view(),
         name="event-update"),

]
