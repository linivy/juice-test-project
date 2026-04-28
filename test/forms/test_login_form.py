import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def close_cookie_banner(page: Page):
    """关闭 Cookie 弹窗"""
    try:
        close_btn = page.locator("button[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass


def test_login_page_loads(page: Page):
    """测试登录页面正常加载"""
    # Arrange
    
    # Act
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    # Assert
    # 使用更通用的选择器查找 Login 标题
    login_heading = page.locator("mat-card h2, mat-card h1, .login-form h2, .login-form h1")
    expect(login_heading.first).to_be_visible(timeout=5000)
    
    # 验证表单元素存在
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#loginButton")).to_be_visible()


def test_login_with_valid_credentials(page: Page):
    """测试使用有效凭据登录"""
    # Arrange
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # Act
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    # Assert
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")


def test_login_with_invalid_credentials(page: Page):
    """测试使用无效凭据登录"""
    # Arrange
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # Act
    page.fill("#email", "invalid@example.com")
    page.fill("#password", "wrongpassword")
    page.click("#loginButton")
    
    # Assert
    # 验证停留在登录页面
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    
    # 验证显示错误消息
    error_message = page.get_by_text("Invalid email or password", exact=False)
    expect(error_message).to_be_visible(timeout=5000)


def test_login_with_empty_credentials(page: Page):
    """测试使用空凭据登录 - 按钮应处于禁用状态"""
    # Arrange
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # Act
    page.fill("#email", "")
    page.fill("#password", "")
    
    # Assert
    # 验证登录按钮处于禁用状态
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    
    # 验证仍停留在登录页面
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)