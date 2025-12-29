# Events Django Project

This is a Django-based web application for managing events, bookings, and users. The project includes authentication, event creation, filtering, and booking management.

## Features

- User registration and login
- Role-based access (organizer, participant)
- Event creation and management
- Booking system for events
- Event filtering by name, type, and location
- Responsive design using Bootstrap 5

## Tech Stack

- Python 3.x
- Django
- SQLite (default database)
- Bootstrap 5 (frontend)
- flake8 (code style and linting)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>

2. Create a virtual environment and activate it:
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
3. Install dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py migrate

## About

This is a Django-based web application for managing events, bookings, and users.  
You can visit the live website here: [https://events-django-project.onrender.com](https://events-django-project.onrender.com/)

Initial Data

The initial_data folder contains CSV files with initial data for the database.
To populate the database, use the custom management command:

  python manage.py import_initial_data
  
This will read the CSV files and create the necessary records for EventType, Location, User, etc.

Running the Development Server

python manage.py runserver

Access the app at http://127.0.0.1:8000/

Tests
Run all tests:

python manage.py test

Code Style
This project uses flake8 for linting and code style checks.
Configuration is in .flake8 file.

License
This project is open source and available under the MIT License.




