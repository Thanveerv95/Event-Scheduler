# 📖 Event Scheduler System Documentation

## Overview
The Event Scheduler System is a modern, minimalist, and user-friendly application built with Python and Flask. It allows users to efficiently manage their events, appointments, meetings, and tasks. The system supports event creation, listing, updating, deletion, reminders, recurring events, search, and email notifications. It is designed for extensibility and ease of use, with both a RESTful API and a beautiful web interface.

---

## Features

### Core Features
- **Event Creation:** Add events with title, description, start time, and end time.
- **Event Listing:** View all scheduled events, sorted by start time (earliest first).
- **Event Updating:** Update any details of an existing event (title, description, time, recurrence).
- **Event Deletion:** Delete events from the system.
- **Persistence:** All events are saved to a file (`events.json`) and loaded on application start.

### Bonus Features
- **Reminders:** System checks every minute and displays reminders for events due within the next hour.
- **Recurring Events:** Support for daily, weekly, or monthly recurring events.
- **Search:** Search for events by title or description.
- **Email Notifications:** (Optional) Send email reminders for upcoming events.
- **Unit Tests:** Comprehensive test suite using Pytest.
- **Modern Web UI:** Minimalist, attractive, and responsive web interface.

---

## Project Structure
```
project-root/
├── app.py                      # Main Flask application
├── test_app.py                 # Unit tests
├── requirements.txt            # Python dependencies
├── README.md                   # Quick start and API usage
├── DOCUMENTATION.md            # (This file) Full documentation
├── Event_Scheduler_API.postman_collection.json # Postman collection
├── templates/
│   └── index.html              # Web interface template
├── events.json                 # Event data storage (auto-generated)
└── .gitignore                  # Files to ignore in version control
```

---

## Setup & Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps
1. **Clone the repository or download the project files.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```
4. **Access the web interface:**
   - Open your browser and go to [http://localhost:5000](http://localhost:5000)

---

## Usage

### Web Interface
- Add, view, update, delete, and search events using the intuitive web UI.
- View statistics for total, upcoming, and today's events.
- All changes are reflected in real-time.

### API Endpoints
Base URL: `http://localhost:5000/api`

| Method | Endpoint                  | Description                                 |
|--------|---------------------------|---------------------------------------------|
| GET    | /health                   | Health check                                |
| GET    | /events                   | List all events                             |
| POST   | /events                   | Create a new event                          |
| GET    | /events/{event_id}        | Get event by ID                             |
| PUT    | /events/{event_id}        | Update event by ID                          |
| DELETE | /events/{event_id}        | Delete event by ID                          |
| GET    | /events/search?q=keyword  | Search events by title or description       |
| GET    | /events/upcoming?hours=n  | Get events due within the next n hours      |

#### Example: Create Event
```http
POST /api/events
Content-Type: application/json
{
  "title": "Team Meeting",
  "description": "Weekly team sync",
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T11:00:00",
  "recurring": "weekly"
}
```

#### Example: Search Events
```http
GET /api/events/search?q=meeting
```

#### Example: Get Upcoming Events
```http
GET /api/events/upcoming?hours=2
```

---

## Testing

- Run all tests:
  ```bash
  pytest test_app.py -v
  ```
- (Optional) Run with coverage:
  ```bash
  pytest test_app.py --cov=app -v
  ```

---

## Postman Collection
- Import `Event_Scheduler_API.postman_collection.json` into Postman to test all API endpoints easily.

---

## Email Notifications (Optional)
- To enable email notifications, update the `EMAIL_CONFIG` in `app.py` with your SMTP server, email, and app password.
- Uncomment the line `self.send_email_notification(event)` in the `check_reminders` method.
- For Gmail, enable 2FA and use an App Password.

---

## Customization & Extensibility
- The code is modular and easy to extend for new features (e.g., user authentication, calendar integration, advanced recurrence, etc.).
- UI can be customized via `templates/index.html`.
- API can be extended by adding new routes in `app.py`.

---

## Troubleshooting
- **Port already in use:** Change the port in `app.py` or stop the process using port 5000.
- **Email not working:** Check SMTP settings and credentials.
- **Import errors:** Reinstall dependencies with `pip install -r requirements.txt --force-reinstall`.
