import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"

def test_login_page_loads(page: Page):
    """测试登录页面正常加载"""
    page.goto(f"{BASE_URL}/#/login")
    
    # 等待页面加载
    page.wait_for_load_state("networkidle")
    
    # 使用更精确的选择器定位 Login 标题
    login_heading = page.locator("h1").filter(has_text="Login")
    expect(login_heading.first).to_be_visible()
    assert "Login" in login_heading.first.inner_text()


def test_login_with_valid_credentials(page: Page):
    """测试使用有效凭据登录"""
    page.goto(f"{BASE_URL}/#/login")
    
    # 先关闭可能出现的 Cookie 弹窗
    try:
        # 等待 cookie 弹窗出现并点击关闭
        close_btn = page.locator("button[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass  # 没有弹窗则跳过
    
    # 填写登录表单
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    
    # 点击登录按钮
    page.click("#loginButton")
    
    # 等待登录成功，跳转到搜索页面
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")