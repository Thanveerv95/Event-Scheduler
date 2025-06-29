from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import schedule
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dateutil import parser
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
EVENTS_FILE = 'events.json'
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',  # Update with your email
    'sender_password': 'your-app-password'   # Update with your app password
}

class EventScheduler:
    def __init__(self):
        self.events = []
        self.load_events()
        self.start_reminder_thread()
    
    def load_events(self):
        """Load events from JSON file"""
        try:
            if os.path.exists(EVENTS_FILE):
                with open(EVENTS_FILE, 'r') as f:
                    self.events = json.load(f)
        except Exception as e:
            print(f"Error loading events: {e}")
            self.events = []
    
    def save_events(self):
        """Save events to JSON file"""
        try:
            with open(EVENTS_FILE, 'w') as f:
                json.dump(self.events, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving events: {e}")
    
    def add_event(self, title, description, start_time, end_time, recurring=None):
        """Add a new event"""
        event = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'start_time': start_time,
            'end_time': end_time,
            'recurring': recurring,
            'created_at': datetime.now().isoformat()
        }
        self.events.append(event)
        self.save_events()
        return event
    
    def get_all_events(self):
        """Get all events sorted by start time"""
        return sorted(self.events, key=lambda x: x['start_time'])
    
    def get_event_by_id(self, event_id):
        """Get event by ID"""
        for event in self.events:
            if event['id'] == event_id:
                return event
        return None
    
    def update_event(self, event_id, **kwargs):
        """Update an existing event"""
        event = self.get_event_by_id(event_id)
        if event:
            for key, value in kwargs.items():
                if key in event:
                    event[key] = value
            self.save_events()
            return event
        return None
    
    def delete_event(self, event_id):
        """Delete an event"""
        event = self.get_event_by_id(event_id)
        if event:
            self.events.remove(event)
            self.save_events()
            return True
        return False
    
    def search_events(self, query):
        """Search events by title or description"""
        query = query.lower()
        results = []
        for event in self.events:
            if (query in event['title'].lower() or 
                query in event['description'].lower()):
                results.append(event)
        return results
    
    def get_upcoming_events(self, hours=1):
        """Get events due within specified hours"""
        now = datetime.now()
        upcoming = []
        for event in self.events:
            start_time = parser.parse(event['start_time'])
            time_diff = start_time - now
            if timedelta(0) <= time_diff <= timedelta(hours=hours):
                upcoming.append(event)
        return upcoming
    
    def send_email_notification(self, event):
        """Send email notification for event reminder"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['sender_email']  # Send to self for demo
            msg['Subject'] = f"Event Reminder: {event['title']}"
            
            body = f"""
            Event Reminder!
            
            Title: {event['title']}
            Description: {event['description']}
            Start Time: {event['start_time']}
            End Time: {event['end_time']}
            
            Don't forget your event!
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_email'], text)
            server.quit()
            
            print(f"Email notification sent for event: {event['title']}")
        except Exception as e:
            print(f"Error sending email notification: {e}")
    
    def check_reminders(self):
        """Check for upcoming events and send reminders"""
        upcoming = self.get_upcoming_events(1)  # Next hour
        for event in upcoming:
            print(f"REMINDER: {event['title']} starts at {event['start_time']}")
            # Uncomment the line below to enable email notifications
            # self.send_email_notification(event)
    
    def start_reminder_thread(self):
        """Start background thread for checking reminders"""
        def reminder_worker():
            schedule.every().minute.do(self.check_reminders)
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        thread = threading.Thread(target=reminder_worker, daemon=True)
        thread.start()

# Initialize the scheduler
scheduler = EventScheduler()

# Web Interface Route
@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

# API Routes
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        events = scheduler.get_all_events()
        return jsonify({'success': True, 'events': events})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'start_time', 'end_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Validate datetime format
        try:
            start_time = parser.parse(data['start_time'])
            end_time = parser.parse(data['end_time'])
        except:
            return jsonify({'success': False, 'error': 'Invalid datetime format'}), 400
        
        # Validate time logic
        if start_time >= end_time:
            return jsonify({'success': False, 'error': 'Start time must be before end time'}), 400
        
        event = scheduler.add_event(
            title=data['title'],
            description=data['description'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            recurring=data.get('recurring')
        )
        
        return jsonify({'success': True, 'event': event}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event"""
    try:
        event = scheduler.get_event_by_id(event_id)
        if event:
            return jsonify({'success': True, 'event': event})
        else:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    try:
        data = request.get_json()
        
        # Validate datetime format if provided
        if 'start_time' in data:
            try:
                parser.parse(data['start_time'])
            except:
                return jsonify({'success': False, 'error': 'Invalid start_time format'}), 400
        
        if 'end_time' in data:
            try:
                parser.parse(data['end_time'])
            except:
                return jsonify({'success': False, 'error': 'Invalid end_time format'}), 400
        
        event = scheduler.update_event(event_id, **data)
        if event:
            return jsonify({'success': True, 'event': event})
        else:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    try:
        success = scheduler.delete_event(event_id)
        if success:
            return jsonify({'success': True, 'message': 'Event deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/search', methods=['GET'])
def search_events():
    """Search events by title or description"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        results = scheduler.search_events(query)
        return jsonify({'success': True, 'events': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Get upcoming events within specified hours"""
    try:
        hours = int(request.args.get('hours', 1))
        events = scheduler.get_upcoming_events(hours)
        return jsonify({'success': True, 'events': events})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'success': True, 'status': 'healthy', 'message': 'Event Scheduler API is running'})

if __name__ == '__main__':
    print("🚀 Starting Event Scheduler System...")
    print("📅 Web interface available at http://localhost:5000")
    print("🔗 API endpoints available at http://localhost:5000/api")
    print("🔔 Reminder system is active (checking every minute)")
    print("📧 Email notifications are disabled by default")
    print("💡 Use Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000) 