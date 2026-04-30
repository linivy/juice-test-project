# test/forms/test_login_form.py
"""
登录模块 - 表单验证自动化测试

对应的功能测试点:
- TC-LOGIN-001: 登录页面正常加载 (优先级: P0)
- TC-LOGIN-002: 使用有效凭据登录成功 (优先级: P0)
- TC-LOGIN-003: 使用无效凭据登录失败 (优先级: P1)
- TC-LOGIN-004: 空凭据验证（按钮禁用状态） (优先级: P1)
- TC-LOGIN-005: 多用户登录验证 (优先级: P1)
- TC-LOGIN-006: 边界值测试 (优先级: P2)
- TC-LOGIN-007: 安全攻击防护（SQL注入/XSS） (优先级: P0)
"""

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


def close_overlay(page: Page):
    """关闭可能遮挡的覆盖层"""
    try:
        page.mouse.click(10, 10)
    except:
        pass


# ==================== TC-LOGIN-001: 登录页面加载测试 ====================

def test_login_page_loads(page: Page):
    """
    【TC-LOGIN-001】登录页面正常加载
    """
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    # 验证页面标题
    login_heading = page.locator("mat-card h2, mat-card h1, .login-form h2, .login-form h1")
    expect(login_heading.first).to_be_visible(timeout=5000)
    
    # 验证表单元素
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#loginButton")).to_be_visible()


# ==================== TC-LOGIN-002: 有效凭据登录 ====================

def test_valid_credentials(page: Page):
    """
    【TC-LOGIN-002】使用有效凭据登录成功
    """
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    # 输入有效凭据
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    
    # 点击登录按钮
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    page.click("#loginButton")
    
    # 验证登录成功
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")


# ==================== TC-LOGIN-003: 无效凭据登录 ====================

def test_invalid_credentials(page: Page):
    """
    【TC-LOGIN-003】使用无效凭据登录失败
    """
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    # 输入无效凭据
    page.fill("#email", "invalid@example.com")
    page.fill("#password", "wrongpassword")
    
    # 点击登录按钮
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    page.click("#loginButton")
    
    # 验证登录失败
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    error_message = page.get_by_text("Invalid email or password", exact=False)
    expect(error_message).to_be_visible(timeout=5000)


# ==================== TC-LOGIN-004: 空凭据验证 ====================

def test_empty_credentials(page: Page):
    """
    【TC-LOGIN-004】空凭据验证 - 按钮处于禁用状态
    """
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 清空输入框
    page.fill("#email", "")
    page.fill("#password", "")
    
    # 验证登录按钮禁用
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)


# ==================== TC-LOGIN-005: 多用户登录验证 ====================

@pytest.mark.parametrize("email,password,role", [
    ("admin@juice-sh.op", "admin123", "管理员"),
    ("jim@juice-sh.op", "ncc-1701", "普通用户"),
    ("bender@juice-sh.op", "OhG0dPlease1nsertLiquor!", "测试用户"),
])
def test_multiple_users(page: Page, email, password, role):
    """
    【TC-LOGIN-005】多用户登录验证
    """
    print(f"\n测试用户: {role} ({email})")
    
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    # 输入凭据
    page.fill("#email", email)
    page.fill("#password", password)
    
    # 点击登录按钮
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    page.click("#loginButton")
    
    # 验证登录成功
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")
    
    print(f"✅ 用户 {role} 登录成功")


# ==================== TC-LOGIN-006: 边界值测试 ====================

@pytest.mark.parametrize("email,password,boundary_type", [
    ("a@b.c", "123456", "最短邮箱地址"),
    ("test@test.com", "1", "最短密码"),
    ("test@test.com", "!@#$%^&*()_+", "特殊字符密码"),
])
def test_boundary_values(page: Page, email, password, boundary_type):
    """
    【TC-LOGIN-006】边界值测试
    """
    print(f"\n测试边界场景: {boundary_type}")
    
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 输入边界值
    page.fill("#email", email)
    page.fill("#password", password)
    
    # 验证系统没有崩溃
    assert not page.is_closed()
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    
    print(f"✅ 边界场景 {boundary_type} 测试通过")


# ==================== TC-LOGIN-007: 安全攻击防护 ====================

@pytest.mark.parametrize("attack_string,password,attack_type", [
    ("' OR '1'='1", "anything", "SQL注入攻击"),
    ("<script>alert('xss')</script>", "password", "XSS攻击"),
    ("admin'--", "anything", "SQL注释注入"),
])
def test_security_attacks(page: Page, attack_string, password, attack_type):
    """
    【TC-LOGIN-007】安全攻击防护
    """
    print(f"\n测试攻击类型: {attack_type}")
    
    # 访问登录页面
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    # 输入攻击向量
    page.fill("#email", attack_string)
    page.fill("#password", password)
    
    # 点击登录按钮
    page.wait_for_selector("#loginButton:not([disabled])", timeout=5000)
    page.click("#loginButton")
    
    # 验证应用正确处理攻击
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    assert page.is_visible("#email")
    assert page.is_visible("#password")
    
    print(f"✅ 攻击类型 {attack_type} 被正确处理")


# ==================== 原有的基础测试（保留兼容） ====================

def test_login_with_valid_credentials(page: Page):
    """测试使用有效凭据登录（兼容保留）"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")


def test_login_with_invalid_credentials(page: Page):
    """测试使用无效凭据登录（兼容保留）"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "invalid@example.com")
    page.fill("#password", "wrongpassword")
    page.click("#loginButton")
    
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    error_message = page.get_by_text("Invalid email or password", exact=False)
    expect(error_message).to_be_visible(timeout=5000)


def test_login_with_empty_credentials(page: Page):
    """测试使用空凭据登录（兼容保留）"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "")
    page.fill("#password", "")
    
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)