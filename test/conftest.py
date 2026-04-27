import pytest
from playwright.sync_api import Page

@pytest.fixture
def logged_in_page(page: Page):
    """已登录的页面 fixture"""
    page.goto("http://localhost:3000/#/login")
    page.wait_for_load_state("networkidle")
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    page.wait_for_url("http://localhost:3000/#/search")
    return page