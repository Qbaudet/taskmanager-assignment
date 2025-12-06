import pytest
import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from models import User, Task


@pytest.fixture
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_register_and_login(client):
    response = client.post("/register", data={
        "username": "testuser",
        "password": "mdp",
        "confirm": "mdp"
    }, follow_redirects=True)

    assert b"Registration successful" in response.data

    response = client.post("/login", data={
        "username": "testuser",
        "password": "mdp"
    }, follow_redirects=True)

    assert b"Logged in successfully" in response.data



def test_create_task(client):
    # we need a user first because the task can only be created if a user is logged in 

    client.post("/register", data={
        "username": "testuser2",
        "password": "mdp2",
        "confirm": "mdp2"
    })

    client.post("/login", data={
        "username": "testuser2",
        "password": "mdp2"
    })

    response = client.post("/tasks/new", data={
        "title": "test task",
        "description": "Testing create",
        "due_date": ""
    }, follow_redirects=True)

    assert b"Task created" in response.data

    task = Task.query.first()
    assert task.title == "test task"



def test_toggle_task(client):
    # we need a user first because the task can only be created if a user is logged in 
    client.post("/register", data={
        "username": "testuser3",
        "password": "mdp3",
        "confirm": "mdp3"
    })

    client.post("/login", data={
        "username": "testuser3",
        "password": "mdp3"
    })

    client.post("/tasks/new", data={"title": "Test", "due_date": ""})

    task = Task.query.first()
    assert task.is_completed is False

    client.post(f"/tasks/{task.id}/toggle", follow_redirects=True)

    task = Task.query.first()
    assert task.is_completed is True
