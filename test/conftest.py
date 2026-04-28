import pytest
from playwright.sync_api import Page, Browser, BrowserContext
import os
from datetime import datetime
import traceback

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
        "locale": "zh-CN",
    }


@pytest.fixture
def context(browser: Browser):
    """创建浏览器上下文"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="test-results/videos/",
        locale="zh-CN",
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """创建页面 - 配置页面级别截图选项"""
    page = context.new_page()
    # 设置页面级别截图选项
    page.set_default_timeout(30000)
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


# ==================== 失败自动截图 Hook ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图和保存日志"""
    outcome = yield
    report = outcome.get_result()
    
    # 只在测试执行阶段(call)失败时截图
    if report.when == "call" and report.failed:
        # 尝试获取 page fixture
        page = item.funcargs.get("page")
        
        if page is None:
            # 尝试从 logged_in_page fixture 获取
            page = item.funcargs.get("logged_in_page")
        
        # 生成时间戳和测试名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace("[", "_").replace("]", "_")  # 清理特殊字符
        
        if page:
            try:
                # 1. 保存页面截图
                screenshot_path = f"test-results/screenshots/{test_name}_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n📸 截图已保存: {screenshot_path}")
                
                # 2. 保存页面 HTML
                html_path = f"test-results/screenshots/{test_name}_{timestamp}.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page.content())
                print(f"📄 HTML 源码已保存: {html_path}")
                
                # 3. 保存控制台日志
                logs = page.evaluate("() => console.logs ? console.logs.join('\n') : 'No console logs'")
                if logs and logs != "No console logs":
                    log_path = f"test-results/logs/{test_name}_{timestamp}.log"
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(logs)
                    print(f"📝 控制台日志已保存: {log_path}")
                    
            except Exception as e:
                print(f"⚠️ 截图时发生错误: {str(e)}")
        
        # 4. 保存测试失败信息到日志文件
        log_path = f"test-results/logs/{test_name}_{timestamp}_error.log"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"测试名称: {item.name}\n")
            f.write(f"测试路径: {item.path}\n")
            f.write(f"失败时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n=== 错误信息 ===\n")
            f.write(str(report.longrepr) + "\n")
            f.write(f"\n=== 堆栈跟踪 ===\n")
            if call.excinfo:
                f.write("\n".join(traceback.format_tb(call.excinfo.tb)))
        print(f"📝 错误日志已保存: {log_path}")