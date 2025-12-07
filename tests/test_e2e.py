import pytest

import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models import Task, User
from app import db


BASE_URL = "http://localhost:5000"

@pytest.mark.e2e
def test_login_flow(page):
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testmdp")
    page.fill('input[name="confirm"]', "testmdp")
    page.click('button[type="submit"]')

    try:
        page.wait_for_url(f"{BASE_URL}/login", timeout=2000)
        page.goto(f"{BASE_URL}/login")

    except:
        page.goto(f"{BASE_URL}/login")

    
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testmdp")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/")

    assert "Your Tasks" in page.content()


@pytest.mark.e2e
def test_create_task(page):
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testmdp")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/")

    page.goto(f"{BASE_URL}/tasks/new")
    page.fill('input[name="title"]', "E2E test task")
    page.fill('textarea[name="description"]', "Created during E2E test")
    page.fill('input[name="due_date"]', "2030-12-31")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/")

    assert "E2E test task" in page.content()


@pytest.mark.e2e
def test_toggle_task(page):
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testmdp")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/")

    task = page.locator("li.task-item", has_text="E2E test task")
    toggle_button = task.locator("button:has-text('Complete')")
    toggle_button.click()
    page.wait_for_timeout(500)

    assert task.locator(".badge.done").is_visible()

    toggle_button = task.locator("button:has-text('Reopen')")
    toggle_button.click()
    page.wait_for_timeout(500)

    assert task.locator(".badge.open").is_visible()


    assert "E2E test task" in page.content()


