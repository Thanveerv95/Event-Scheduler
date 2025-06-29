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

## 🚀 Quick Start

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

## 🧪 Running Tests

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

## 📱 Postman Collection

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

## 🐛 Troubleshooting

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

