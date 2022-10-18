import pytest
from src import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_should_status_code_ok(client):
	response = client.get('/plate')
	assert response.status_code == 200
