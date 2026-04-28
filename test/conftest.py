import pytest
from playwright.sync_api import Page, Browser, BrowserContext

BASE_URL = "http://localhost:3000"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文参数"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "test-results/videos/",
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture
def context(browser: Browser):
    """创建浏览器上下文"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="test-results/videos/",
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """创建页面"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def logged_in_page(page: Page):
    """提供已登录的页面 fixture"""
    # Arrange
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    # 关闭欢迎弹窗
    try:
        close_btn = page.locator("[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass
    
    # 登录
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.press("#password", "Enter")
    
    # 等待登录成功
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    
    yield page


@pytest.fixture
def api_request_context(context: BrowserContext):
    """提供 API 请求上下文（已认证）"""
    # 先登录以获取认证 cookie
    page = context.new_page()
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.press("#password", "Enter")
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    
    # 创建 API 请求上下文，继承浏览器的 cookie
    api_context = context.request
    
    page.close()
    return api_context