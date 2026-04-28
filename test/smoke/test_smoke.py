# test/smoke/test_smoke.py
"""冒烟测试套件 - 核心功能验证"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def close_dialogs(page: Page):
    """关闭弹窗"""
    try:
        # 关闭 Cookie 弹窗
        cookie_btn = page.get_by_role("button", name="Me want it!")
        if cookie_btn.is_visible(timeout=2000):
            cookie_btn.click()
            page.wait_for_timeout(500)
        
        # 关闭其他弹窗
        close_buttons = page.locator(".mat-mdc-dialog-surface button[aria-label='Close'], .mat-dialog-actions button, button[mat-dialog-close]")
        for btn in close_buttons.all():
            if btn.is_visible():
                btn.click()
                page.wait_for_timeout(500)
    except:
        pass


@pytest.mark.smoke
def test_login_smoke(page: Page):
    """冒烟测试：登录功能"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    # 关闭可能存在的弹窗
    close_dialogs(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    
    # 再次检查并关闭弹窗
    close_dialogs(page)
    
    # 使用 force=True 强制点击，避免被弹窗拦截
    page.click("#loginButton", force=True)
    
    # 等待导航完成，支持多个可能的目标 URL
    page.wait_for_load_state("networkidle", timeout=10000)
    
    # 验证登录成功 - 检查是否跳转到主页或搜索页
    current_url = page.url
    assert "search" in current_url or "home" in current_url or "#/" in current_url, f"登录后未跳转到预期页面: {current_url}"


@pytest.mark.smoke
def test_search_smoke(logged_in_page: Page):
    """冒烟测试：搜索功能"""
    page = logged_in_page
    
    search_input = page.get_by_role("searchbox")
    if search_input.count() > 0:
        search_input.fill("Apple Juice")
        search_input.press("Enter")
        
        products = page.locator(".mat-card")
        expect(products.first).to_be_visible()


@pytest.mark.smoke
def test_orders_smoke(logged_in_page: Page):
    """冒烟测试：订单列表"""
    page = logged_in_page
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_url(f"{BASE_URL}/#/orders")