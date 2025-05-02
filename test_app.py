
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Security Header Checker!' in response.data

def test_check_endpoint_valid_url(client):
    response = client.post('/check', json={'url': 'https://www.example.com'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert json_data['url'] == 'https://www.example.com'

def test_check_endpoint_no_url(client):
    response = client.post('/check', json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'URL is required'

def test_check_endpoint_invalid_url(client):
    response = client.post('/check', json={'url': 'invalid-url'})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Invalid URL format'