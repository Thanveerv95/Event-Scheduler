import pytest
import json
import os
from datetime import datetime, timedelta
from app import app, EventScheduler

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def scheduler():
    """Create a test scheduler instance"""
    return EventScheduler()

@pytest.fixture
def sample_event_data():
    """Sample event data for testing"""
    now = datetime.now()
    return {
        'title': 'Test Meeting',
        'description': 'A test meeting for unit testing',
        'start_time': (now + timedelta(hours=1)).isoformat(),
        'end_time': (now + timedelta(hours=2)).isoformat(),
        'recurring': 'daily'
    }

class TestEventScheduler:
    """Test cases for EventScheduler class"""
    
    def test_add_event(self, scheduler, sample_event_data):
        """Test adding a new event"""
        event = scheduler.add_event(**sample_event_data)
        
        assert event['title'] == sample_event_data['title']
        assert event['description'] == sample_event_data['description']
        assert 'id' in event
        assert 'created_at' in event
    
    def test_get_all_events(self, scheduler, sample_event_data):
        """Test getting all events"""
        # Add multiple events
        event1 = scheduler.add_event(**sample_event_data)
        
        sample_event_data['title'] = 'Earlier Meeting'
        sample_event_data['start_time'] = (datetime.now() + timedelta(minutes=30)).isoformat()
        event2 = scheduler.add_event(**sample_event_data)
        
        events = scheduler.get_all_events()
        
        assert len(events) >= 2
        # Check if events are sorted by start time
        assert events[0]['start_time'] <= events[1]['start_time']
    
    def test_get_event_by_id(self, scheduler, sample_event_data):
        """Test getting event by ID"""
        event = scheduler.add_event(**sample_event_data)
        retrieved_event = scheduler.get_event_by_id(event['id'])
        
        assert retrieved_event is not None
        assert retrieved_event['id'] == event['id']
        assert retrieved_event['title'] == event['title']
    
    def test_update_event(self, scheduler, sample_event_data):
        """Test updating an event"""
        event = scheduler.add_event(**sample_event_data)
        updated_title = 'Updated Meeting Title'
        
        updated_event = scheduler.update_event(event['id'], title=updated_title)
        
        assert updated_event is not None
        assert updated_event['title'] == updated_title
        assert updated_event['description'] == sample_event_data['description']
    
    def test_delete_event(self, scheduler, sample_event_data):
        """Test deleting an event"""
        event = scheduler.add_event(**sample_event_data)
        initial_count = len(scheduler.events)
        
        success = scheduler.delete_event(event['id'])
        
        assert success is True
        assert len(scheduler.events) == initial_count - 1
        assert scheduler.get_event_by_id(event['id']) is None
    
    def test_search_events(self, scheduler, sample_event_data):
        """Test searching events"""
        event = scheduler.add_event(**sample_event_data)
        
        # Search by title
        results = scheduler.search_events('Test Meeting')
        assert len(results) >= 1
        assert results[0]['title'] == 'Test Meeting'
        
        # Search by description
        results = scheduler.search_events('unit testing')
        assert len(results) >= 1
        assert 'unit testing' in results[0]['description'].lower()
    
    def test_get_upcoming_events(self, scheduler, sample_event_data):
        """Test getting upcoming events"""
        # Event in next hour
        event = scheduler.add_event(**sample_event_data)
        
        upcoming = scheduler.get_upcoming_events(hours=1)
        assert len(upcoming) >= 1
        
        # Event in next 2 hours (should not appear in 1-hour search)
        sample_event_data['start_time'] = (datetime.now() + timedelta(hours=1.5)).isoformat()
        sample_event_data['end_time'] = (datetime.now() + timedelta(hours=2.5)).isoformat()
        scheduler.add_event(**sample_event_data)
        
        upcoming = scheduler.get_upcoming_events(hours=1)
        assert len(upcoming) >= 1

class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['status'] == 'healthy'
    
    def test_create_event(self, client, sample_event_data):
        """Test creating an event via API"""
        response = client.post('/api/events', 
                             data=json.dumps(sample_event_data),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 201
        assert data['success'] is True
        assert data['event']['title'] == sample_event_data['title']
    
    def test_create_event_missing_fields(self, client):
        """Test creating event with missing required fields"""
        incomplete_data = {'title': 'Test Event'}
        response = client.post('/api/events',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Missing required field' in data['error']
    
    def test_create_event_invalid_time(self, client):
        """Test creating event with invalid time format"""
        invalid_data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'start_time': 'invalid-time',
            'end_time': 'invalid-time'
        }
        response = client.post('/api/events',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Invalid datetime format' in data['error']
    
    def test_get_all_events(self, client, sample_event_data):
        """Test getting all events via API"""
        # First create an event
        client.post('/api/events',
                   data=json.dumps(sample_event_data),
                   content_type='application/json')
        
        response = client.get('/api/events')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert 'events' in data
        assert len(data['events']) >= 1
    
    def test_get_event_by_id(self, client, sample_event_data):
        """Test getting specific event via API"""
        # Create an event
        create_response = client.post('/api/events',
                                    data=json.dumps(sample_event_data),
                                    content_type='application/json')
        event_id = json.loads(create_response.data)['event']['id']
        
        # Get the event
        response = client.get(f'/api/events/{event_id}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['event']['id'] == event_id
    
    def test_update_event(self, client, sample_event_data):
        """Test updating an event via API"""
        # Create an event
        create_response = client.post('/api/events',
                                    data=json.dumps(sample_event_data),
                                    content_type='application/json')
        event_id = json.loads(create_response.data)['event']['id']
        
        # Update the event
        update_data = {'title': 'Updated Title'}
        response = client.put(f'/api/events/{event_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['event']['title'] == 'Updated Title'
    
    def test_delete_event(self, client, sample_event_data):
        """Test deleting an event via API"""
        # Create an event
        create_response = client.post('/api/events',
                                    data=json.dumps(sample_event_data),
                                    content_type='application/json')
        event_id = json.loads(create_response.data)['event']['id']
        
        # Delete the event
        response = client.delete(f'/api/events/{event_id}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert 'deleted successfully' in data['message']
    
    def test_search_events(self, client, sample_event_data):
        """Test searching events via API"""
        # Create an event
        client.post('/api/events',
                   data=json.dumps(sample_event_data),
                   content_type='application/json')
        
        # Search for events
        response = client.get('/api/events/search?q=Test Meeting')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['events']) >= 1
    
    def test_search_events_no_query(self, client):
        """Test searching events without query parameter"""
        response = client.get('/api/events/search')
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Search query is required' in data['error']
    
    def test_get_upcoming_events(self, client, sample_event_data):
        """Test getting upcoming events via API"""
        # Create an event
        client.post('/api/events',
                   data=json.dumps(sample_event_data),
                   content_type='application/json')
        
        # Get upcoming events
        response = client.get('/api/events/upcoming?hours=1')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert 'events' in data

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 