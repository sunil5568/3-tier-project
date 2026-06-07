import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_status_code(client):
    """Test that the homepage loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
