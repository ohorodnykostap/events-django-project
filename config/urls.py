from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("event_service.urls", namespace="events")),
    path("accounts/", include("django.contrib.auth.urls")),
]
