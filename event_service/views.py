from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventType, Location, Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, EventForm, CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView)
from django.contrib import messages


class EventListView(ListView):
    model = Event
    template_name = "event_service/event_list.html"
    context_object_name = "events"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_types"] = EventType.objects.all()
        context["locations"] = Location.objects.all()

        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["query_string"] = query_params.urlencode()
        return context

    def get_queryset(self):
        queryset = Event.objects.all().order_by("event_datetime")
        search_query = self.request.GET.get("q")
        event_type_id = self.request.GET.get("event_type")
        location_id = self.request.GET.get("location")

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if event_type_id:
            queryset = queryset.filter(event_type_id=event_type_id)
        if location_id:
            queryset = queryset.filter(location_id=location_id)

        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = "event_service/event_detail.html"
    context_object_name = "event"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "event_service/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["now"] = timezone.now()
        context["user_form"] = CustomUserChangeForm(instance=user)

        if user.role == "participant":
            context["booked_events"] = Booking.objects.filter(user=user)
        elif user.role == "organizer":
            context["organized_events"] = Event.objects.filter(organizer=user)
            context["booked_events"] = Booking.objects.filter(user=user)

        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request,
                           "There was a problem updating your profile.")
        return redirect("events:profile")


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event_service/event_update.html"
    success_url = reverse_lazy("events:profile")

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.event.capacity += 1
    booking.event.save()
    booking.delete()
    return redirect("events:profile")


@login_required
def booking_create(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.available_seats() <= 0:
        messages.error(request, f"No available seats for '{event.name}'.")
        return redirect("events:event-detail", pk=pk)

    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, f"You already booked '{event.name}'.")
        return redirect("events:event-detail", pk=pk)

    Booking.objects.create(user=request.user, event=event)
    messages.success(request, f"Booking for '{event.name}' successful!")
    return redirect("events:event-detail", pk=pk)


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    event = booking.event
    booking.delete()
    messages.success(request,
                     f"Booking for '{event.name}' has been cancelled.")
    return redirect("events:profile")


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_service/event_create.html"
    success_url = reverse_lazy("events:event-list")
    login_url = "login"

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)
