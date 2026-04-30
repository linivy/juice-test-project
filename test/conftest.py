# test/conftest.py
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
import os
from datetime import datetime

# 修正导入路径 - 添加 test.
from test.config.environment import get_config, pytest_addoption as env_pytest_addoption

# 确保测试结果目录存在
os.makedirs("test-results/screenshots", exist_ok=True)
os.makedirs("test-results/videos", exist_ok=True)
os.makedirs("test-results/logs", exist_ok=True)


# ==================== 命令行参数 ====================

def pytest_addoption(parser):
    """添加 pytest 命令行参数"""
    env_pytest_addoption(parser)


# ==================== 环境配置 Fixtures ====================

@pytest.fixture(scope="session")
def app_config(request):
    """获取应用配置"""
    env_name = request.config.getoption("--env")
    return get_config(env_name)


@pytest.fixture(scope="session")
def base_url(app_config):
    """获取基础 URL"""
    return app_config.base_url


# ==================== 浏览器 Fixtures ====================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, app_config):
    """配置浏览器上下文参数 - 支持多环境"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "test-results/videos/",
        "record_video_size": {"width": 1280, "height": 720},
        "ignore_https_errors": not app_config.headless,
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
def page(context: BrowserContext, app_config):
    """创建页面 - 支持多环境超时配置"""
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


# ==================== 共享测试数据 Fixtures ====================

@pytest.fixture
def shared_login_invalid_data():
    """共享的无效登录测试数据"""
    return [
        ("invalid@example.com", "wrongpassword", "Invalid email or password", "错误邮箱+错误密码"),
        ("", "admin123", "Email is required", "空邮箱+正确密码"),
        ("admin@juice-sh.op", "", "Password is required", "正确邮箱+空密码"),
    ]


def generate_large_login_data(count: int = 20):
    """动态生成大量登录测试数据"""
    import random
    import string
    
    test_data = []
    for i in range(count):
        email = f"test_{i}@example.com"
        password = ''.join(random.choices(string.ascii_letters, k=8))
        expected = "Invalid email or password"
        test_data.append((email, password, expected))
    return test_data


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