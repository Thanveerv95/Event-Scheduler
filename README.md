# 📅 Event Scheduler System

A modern, beautiful, and minimalist Event Scheduler System built with Python Flask. This application allows users to manage their events, meetings, and tasks efficiently with features like reminders, recurring events, search functionality, and email notifications.

## ✨ Features

### Core Features
- ✅ **Event Creation**: Add events with title, description, start time, and end time
- ✅ **Event Listing**: View all events sorted by start time (earliest first)
- ✅ **Event Updating**: Modify any details of existing events
- ✅ **Event Deletion**: Remove events from the system
- ✅ **Persistence**: Events are automatically saved to JSON file and loaded on startup

### Bonus Features
- ✅ **Unit Tests**: Comprehensive test suite using Pytest
- ✅ **Reminders**: Automatic reminders for events due within the next hour
- ✅ **Recurring Events**: Support for daily, weekly, or monthly recurring events
- ✅ **Email Notifications**: Email reminders for upcoming events
- ✅ **Search Functionality**: Search events by title or description
- ✅ **Modern API**: RESTful API with proper error handling

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # If you have git installed
   git clone <repository-url>
   cd event-scheduler-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the API**
   - The server will start at `http://localhost:5000`
   - API endpoints are available at `http://localhost:5000/api/`

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "message": "Event Scheduler API is running"
}
```

#### 2. Get All Events
```http
GET /events
```
**Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": "uuid",
      "title": "Team Meeting",
      "description": "Weekly team sync",
      "start_time": "2024-01-15T10:00:00",
      "end_time": "2024-01-15T11:00:00",
      "recurring": "weekly",
      "created_at": "2024-01-14T15:30:00"
    }
  ]
}
```

#### 3. Create Event
```http
POST /events
Content-Type: application/json

{
  "title": "Team Meeting",
  "description": "Weekly team sync meeting",
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T11:00:00",
  "recurring": "weekly"
}
```
**Response:**
```json
{
  "success": true,
  "event": {
    "id": "uuid",
    "title": "Team Meeting",
    "description": "Weekly team sync meeting",
    "start_time": "2024-01-15T10:00:00",
    "end_time": "2024-01-15T11:00:00",
    "recurring": "weekly",
    "created_at": "2024-01-14T15:30:00"
  }
}
```

#### 4. Get Event by ID
```http
GET /events/{event_id}
```

#### 5. Update Event
```http
PUT /events/{event_id}
Content-Type: application/json

{
  "title": "Updated Meeting Title",
  "description": "Updated description"
}
```

#### 6. Delete Event
```http
DELETE /events/{event_id}
```

#### 7. Search Events
```http
GET /events/search?q=meeting
```

#### 8. Get Upcoming Events
```http
GET /events/upcoming?hours=2
```

##  Data Persistence

### How It Works
- **Automatic Saving**: All events are automatically saved to `events.json` file
- **Data Persistence**: Events persist between application restarts
- **JSON Storage**: Human-readable JSON format for easy debugging
- **Error Handling**: Graceful handling of file read/write errors

### Implementation Details
```python
# Events are saved automatically after each operation
def save_events(self):
    """Save events to JSON file"""
    with open(EVENTS_FILE, 'w') as f:
        json.dump(self.events, f, indent=2, default=str)

# Events are loaded on application startup
def load_events(self):
    """Load events from JSON file"""
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as f:
            self.events = json.load(f)
```

##  Postman Collection

### Complete API Testing Suite
The project includes a comprehensive Postman collection with all endpoints:

#### Available Requests:
1. **Health Check** - Verify API is running
2. **Get All Events** - Retrieve all events
3. **Create Event** - Add new event with full details
4. **Create Daily Standup** - Example recurring daily event
5. **Create Monthly Review** - Example recurring monthly event
6. **Get Event by ID** - Retrieve specific event
7. **Update Event** - Modify event details
8. **Update Event Title Only** - Partial update example
9. **Delete Event** - Remove event from system
10. **Search Events** - Find events by keyword
11. **Search Events - Team** - Specific search example
12. **Get Upcoming Events - 1 Hour** - Events due within 1 hour
13. **Get Upcoming Events - 2 Hours** - Events due within 2 hours
14. **Get Upcoming Events - 24 Hours** - Events due within 24 hours

### How to Use Postman Collection:
1. **Import Collection**: Open Postman → Import → Select `Event_Scheduler_API.postman_collection.json`
2. **Start Server**: Run `python app.py`
3. **Test Endpoints**: Click on any request in the collection and send
4. **Variables**: Use `{{event_id}}` variable for dynamic event IDs

### Example Postman Workflow:
1. **Health Check** → Verify API is running
2. **Create Event** → Add a new event
3. **Get All Events** → See your event in the list
4. **Get Event by ID** → Use the returned event ID
5. **Update Event** → Modify the event
6. **Search Events** → Find events by keyword
7. **Delete Event** → Remove the event

## 📧 Email Notifications

### Current Status
- **Disabled by Default**: Email notifications are commented out for security
- **Code Ready**: Full email functionality is implemented
- **Easy to Enable**: Simple configuration change

### How to Enable Email Notifications:

1. **Update Email Configuration** in `app.py`:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password'
}
```

2. **Enable Email Sending** in `app.py`:
```python
def check_reminders(self):
    upcoming = self.get_upcoming_events(1)
    for event in upcoming:
        print(f"REMINDER: {event['title']} starts at {event['start_time']}")
        # Uncomment the line below to enable email notifications
        self.send_email_notification(event)  # ← Uncomment this line
```

3. **Gmail Setup** (if using Gmail):
   - Enable 2-Factor Authentication
   - Generate App Password
   - Use App Password instead of regular password

### Email Features:
- **Automatic Sending**: Emails sent for events due within 1 hour
- **Rich Content**: Includes event title, description, start/end times
- **Error Handling**: Graceful handling of email failures
- **Customizable**: Easy to modify email template and timing

##  Running Tests

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage (if pytest-cov is installed)
pytest test_app.py --cov=app -v
```

## 📧 Email Notifications Setup

To enable email notifications:

1. **Update email configuration in `app.py`:**
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587,
       'sender_email': 'your-email@gmail.com',
       'sender_password': 'your-app-password'
   }
   ```

2. **Enable email notifications:**
   - Uncomment the line `self.send_email_notification(event)` in the `check_reminders` method

3. **For Gmail:**
   - Enable 2-factor authentication
   - Generate an App Password
   - Use the App Password instead of your regular password

##  Postman Collection

### Import the following collection into Postman:

```json
{
  "info": {
    "name": "Event Scheduler API",
    "description": "Complete API collection for Event Scheduler System"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/health"
      }
    },
    {
      "name": "Get All Events",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/events"
      }
    },
    {
      "name": "Create Event",
      "request": {
        "method": "POST",
        "url": "http://localhost:5000/api/events",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"Team Meeting\",\n  \"description\": \"Weekly team sync\",\n  \"start_time\": \"2024-01-15T10:00:00\",\n  \"end_time\": \"2024-01-15T11:00:00\",\n  \"recurring\": \"weekly\"\n}"
        }
      }
    },
    {
      "name": "Get Event by ID",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/events/{{event_id}}"
      }
    },
    {
      "name": "Update Event",
      "request": {
        "method": "PUT",
        "url": "http://localhost:5000/api/events/{{event_id}}",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"Updated Meeting Title\",\n  \"description\": \"Updated description\"\n}"
        }
      }
    },
    {
      "name": "Delete Event",
      "request": {
        "method": "DELETE",
        "url": "http://localhost:5000/api/events/{{event_id}}"
      }
    },
    {
      "name": "Search Events",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/events/search?q=meeting"
      }
    },
    {
      "name": "Get Upcoming Events",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/events/upcoming?hours=2"
      }
    }
  ]
}
```

##  Usage Examples

### Example 1: Create a Daily Standup Meeting
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily Standup",
    "description": "Daily team standup meeting",
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T09:15:00",
    "recurring": "daily"
  }'
```

### Example 2: Search for Meetings
```bash
curl "http://localhost:5000/api/events/search?q=meeting"
```

### Example 3: Get Events in Next 2 Hours
```bash
curl "http://localhost:5000/api/events/upcoming?hours=2"
```

## 🔧 Configuration

### Environment Variables (Optional)
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Custom port number (default: 5000)

### File Storage
- Events are stored in `events.json` file
- The file is automatically created on first run
- Data persists between application restarts

##  Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Import errors:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Email notifications not working:**
   - Check email configuration in `app.py`
   - Ensure SMTP settings are correct
   - Verify app password for Gmail

##  Project Structure

```
event-scheduler-system/
├── app.py              # Main Flask application
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── events.json        # Event data storage (auto-generated)
└── .gitignore         # Git ignore file
```

