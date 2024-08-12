from fastapi.testclient import TestClient
from .main_6 import app


client = TestClient(app)

data = {
    "name": "Husanboy",
    "due_date": "Today",
    "description": "string"
}


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


def test_todo_create():
    response = client.post('/todo/', json=data)
    assert response.status_code == 200
    assert response.json() == data


def test_get_all_todo():
    response = client.get('/todo/', json=data)
    assert response.status_code == 200
    assert data in response.json()


def test_get_todo():
    response = client.get('/todo/0')
    assert response.status_code == 200
    assert response.json() == data


def test_update_todo():
    response = client.put('/todo/1', json={
        "name": "Test",
        "due_date": "Now",
        "description": "Python"
    })
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test",
        "due_date": "Now",
        "description": "Python"
    }


def test_delete_todo():
    response = client.delete('/todo/0')
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test",
        "due_date": "Now",
        "description": "Python"
    }


