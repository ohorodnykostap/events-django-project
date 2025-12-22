# event_service/management/commands/import_initial_data.py
import csv
import os
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from event_service.models import EventType, Location, Event

User = get_user_model()

class Command(BaseCommand):
    help = "Import initial data from CSV files in initial_data/ folder"

    def handle(self, *args, **options):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.data_dir = os.path.join(self.BASE_DIR, 'initial_data')

        self.import_users()
        self.import_event_types()
        self.import_locations()
        self.import_events()
        self.stdout.write(self.style.SUCCESS("Initial data imported successfully!"))

    def import_users(self):
        filepath = os.path.join(self.data_dir, 'users.csv')
        try:
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not User.objects.filter(username=row['username']).exists():
                        user = User(
                            username=row['username'],
                            email=row['email'],
                            is_superuser=row['is_superuser'] == 'True',
                            is_staff=row['is_staff'] == 'True',
                            role=row.get('role', 'participant')
                        )
                        user.set_password(row['password'])
                        user.save()
                        self.stdout.write(f"User {row['username']} created")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"{filepath} not found!"))

    def import_event_types(self):
        filepath = os.path.join(self.data_dir, 'event_types.csv')
        try:
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    obj, created = EventType.objects.get_or_create(name=row['name'])
                    if created:
                        self.stdout.write(f"EventType {row['name']} created")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"{filepath} not found!"))

    def import_locations(self):
        filepath = os.path.join(self.data_dir, 'locations.csv')
        try:
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    obj, created = Location.objects.get_or_create(
                        name=row['name'],
                        address=row['address'],
                    )
                    if created:
                        self.stdout.write(f"Location {row['name']} created")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"{filepath} not found!"))

    def import_events(self):
        filepath = os.path.join(self.data_dir, 'events.csv')
        try:
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        event_type = EventType.objects.get(name=row['event_type'])
                        location = Location.objects.get(name=row['location'])
                        organizer = User.objects.get(username=row['organizer'])
                        event_datetime = datetime.strptime(row['event_datetime'], "%Y-%m-%d %H:%M")
                        price = Decimal(row['price'])
                        capacity = int(row['capacity'])
                        obj, created = Event.objects.get_or_create(
                            name=row['name'],
                            description=row['description'],
                            event_datetime=event_datetime,
                            price=price,
                            capacity=capacity,
                            status=row['status'],
                            event_type=event_type,
                            location=location,
                            organizer=organizer
                        )
                        if created:
                            self.stdout.write(f"Event {row['name']} created")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating event {row.get('name', '?')}: {e}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"{filepath} not found!"))
