# test/conftest.py
import pytest
from playwright.sync_api import Page

@pytest.fixture
def base_url():
    return "http://localhost:3000"

@pytest.fixture
def logged_in_page(page: Page, base_url):
    """已登录的页面 fixture"""
    page.goto(f"{base_url}/#/login")
    try:
        page.locator("button[aria-label='Close Welcome Banner']").click(timeout=2000)
    except:
        pass
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    page.wait_for_url(f"{base_url}/#/search")
    return page