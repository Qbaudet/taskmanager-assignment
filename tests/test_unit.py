import os
import sys
from datetime import date, timedelta
import pytest



sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import _build_postgres_uri
from models import User, Task


def test_user_password():
    testuser = User(username="testuser")
    testuser.set_password("testpwd")

    #we check if the encryuption works
    assert testuser.password_hash != "testpwd"

    #we check if check_password works
    assert testuser.check_password("testpwd") is True
    assert testuser.check_password("wrongpass") is False

def test_task_overdue():
    # past task not completed
    task1 = Task(title="Task 1", due_date=date.today() - timedelta(days=1), is_completed=False)
    assert task1.is_overdue() is True
    # future task not completed
    task3 = Task(title="Task 2", due_date=date.today() + timedelta(days=1), is_completed=False)
    assert task3.is_overdue() is False
    # completed task
    task4 = Task(title="Task 3", due_date=date.today() - timedelta(days=1), is_completed=True)
    assert task4.is_overdue() is False
    # no due date
    task5 = Task(title="Task 4", due_date=None, is_completed=False)
    assert task5.is_overdue() is False

@pytest.mark.unit
def test_build_postgres_uri(monkeypatch):
    #deactive the database that is set in the cicd pipeline
    monkeypatch.delenv("DATABASE_URL", raising=False)

    #temporary false environment variables
    monkeypatch.setenv("POSTGRES_USER", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "pwd")
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setenv("POSTGRES_DB", "database")

    uri = _build_postgres_uri()
    print("URI =", uri)
    assert uri == "postgresql+psycopg2://test:pwd@localhost:5433/database"