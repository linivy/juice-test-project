# 读取 conftest.py
"""test/conftest.py"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
import os
import time

BASE_URL = os.getenv("JUICE_SHOP_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def browser():
    """创建浏览器实例"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser):
    """创建浏览器上下文"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """创建页面实例"""
    page = context.new_page()
    yield page


@pytest.fixture
def mock_page(page: Page):
    """提供带有 Mock 支持的页面"""
    yield page
    page.unroute("**/*")


@pytest.fixture
def logged_in_page(page: Page):
    """已登录的页面 fixture"""
    page.goto(f"{BASE_URL}/#/login")
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.press("#password", "Enter")
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = None
        for fixture in item.fixturenames:
            if fixture == "page" or fixture == "mock_page":
                page = item.funcargs.get(fixture)
                break
        
        if page:
            screenshot_dir = "test-results/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            test_name = item.name.replace("[", "_").replace("]", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"测试失败，截图已保存到: {screenshot_path}")
