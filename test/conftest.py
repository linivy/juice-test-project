# test/conftest.py
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
import os
from datetime import datetime
from config.environment import get_config, pytest_addoption as env_pytest_addoption

BASE_URL = "http://localhost:3000"

# 确保测试结果目录存在
os.makedirs("test-results/screenshots", exist_ok=True)
os.makedirs("test-results/videos", exist_ok=True)
os.makedirs("test-results/logs", exist_ok=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文参数 - 启用视频录制"""
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
    page.set_default_timeout(30000)
    yield page
    page.close()


@pytest.fixture
def logged_in_page(page: Page):
    """提供已登录的页面 fixture"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    try:
        close_btn = page.locator("[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.press("#password", "Enter")
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    
    yield page


# ==================== 失败自动截图 Hook ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace("[", "_").replace("]", "_")
        
        try:
            page = item.funcargs.get("page", None)
            if page is None:
                page = item.funcargs.get("logged_in_page", None)
            
            if page:
                screenshot_path = f"test-results/screenshots/{test_name}_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n📸 截图已保存: {screenshot_path}")
        except Exception:
            pass

# 合并命令行参数
def pytest_addoption(parser):
    env_pytest_addoption(parser)
    # 其他已有的选项...


@pytest.fixture(scope="session")
def app_config():
    """获取应用配置"""
    import os
    env = os.environ.get("TEST_ENV", "local")
    return get_config(env)


@pytest.fixture(scope="session")
def base_url(app_config):
    """获取基础 URL"""
    return app_config.base_url


# 修改原有的 page fixture
@pytest.fixture
def page(context: BrowserContext, app_config):
    """创建页面 - 支持多环境"""
    page = context.new_page()
    page.set_default_timeout(app_config.page_timeout)
    yield page
    page.close()


@pytest.fixture
def logged_in_page(page: Page, app_config, base_url):
    """提供已登录的页面 fixture - 支持多环境"""
    page.goto(f"{base_url}/#/login")
    page.wait_for_load_state("networkidle")
    
    # 关闭 Cookie 弹窗
    try:
        close_btn = page.locator("[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass
    
    # 使用配置中的测试账号登录
    page.fill("#email", app_config.test_user_email)
    page.fill("#password", app_config.test_user_password)
    page.press("#password", "Enter")
    page.wait_for_url(f"{base_url}/#/search", timeout=app_config.page_timeout)
    
    yield page