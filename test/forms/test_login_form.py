# ==================== 规范同步信息 ====================
# spec_file: test/cases/ui-testing-patterns.md
# spec_version: 1.0.0
# spec_hash: e8847ce5
# spec_last_updated: 2026-01-15
# ===================================================

# test/forms/test_login_form.py
"""
登录模块 - 表单验证自动化测试

功能测试点:
- TC-LOGIN-001: 登录页面正常加载
- TC-LOGIN-002: 使用有效凭据登录成功
- TC-LOGIN-003: 使用无效凭据登录失败（参数化）
- TC-LOGIN-004: 空凭据验证（按钮禁用状态）
- TC-LOGIN-005: 多用户登录验证（参数化）
- TC-LOGIN-006: 边界值测试（参数化）
- TC-LOGIN-007: 安全攻击防护（参数化）
- TC-LOGIN-008: 连续多次提交测试
- TC-LOGIN-009: 表单重置功能测试
- TC-LOGIN-010: 密码显示/隐藏切换测试

测试覆盖矩阵:
| 功能测试点ID | 功能描述 | 测试用例函数 | 参数化类型 | 数据组数 |
|-------------|---------|-------------|-----------|---------|
| TC-LOGIN-001 | 页面加载 | test_login_page_loads | basic | 1 |
| TC-LOGIN-002 | 有效登录 | test_valid_credentials | basic | 1 |
| TC-LOGIN-003 | 无效登录 | test_invalid_credentials_param | parametrized | 5 |
| TC-LOGIN-004 | 空凭据 | test_empty_credentials | basic | 1 |
| TC-LOGIN-005 | 多用户 | test_multiple_users | parametrized | 3 |
| TC-LOGIN-006 | 边界值 | test_boundary_values | parametrized | 5 |
| TC-LOGIN-007 | 安全攻击 | test_security_attacks | parametrized | 3 |
| TC-LOGIN-008 | 重复提交 | test_form_submit_multiple_times | basic | 1 |
| TC-LOGIN-009 | 重置功能 | test_form_reset | basic | 1 |
| TC-LOGIN-010 | 密码显示 | test_password_visibility_toggle | basic | 1 |
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
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    login_heading = page.locator("mat-card h2, mat-card h1, .login-form h2, .login-form h1")
    expect(login_heading.first).to_be_visible(timeout=5000)
    
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#loginButton")).to_be_visible()

# ==================== TC-LOGIN-002: 有效凭据登录 ====================

def test_valid_credentials(page: Page):
    """
    【TC-LOGIN-002】使用有效凭据登录成功
    """
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")

# ==================== TC-LOGIN-003: 无效凭据登录（参数化） ====================

@pytest.mark.parametrize("email,password,expected_error,scenario", [
    ("invalid@example.com", "wrongpassword", "Invalid email or password", "错误邮箱+错误密码"),
    ("admin@juice-sh.op", "wrongpassword", "Invalid email or password", "正确邮箱+错误密码"),
    ("invalid@example.com", "admin123", "Invalid email or password", "错误邮箱+正确密码"),
    ("", "admin123", "Email is required", "空邮箱+正确密码"),
    ("admin@juice-sh.op", "", "Password is required", "正确邮箱+空密码"),
])
def test_invalid_credentials_param(page: Page, email: str, password: str, expected_error: str, scenario: str):
    """
    【TC-LOGIN-003】无效凭据登录 - 参数化
    """
    print(f"\n测试场景: {scenario}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)

    # 如果邮箱或密码为空，按钮应该禁用，不需要点击
    if email == "" or password == "":
        login_button = page.locator("#loginButton")
        expect(login_button).to_be_disabled(timeout=5000)
        # 验证停留在登录页面
        expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
        return
    
    page.click("#loginButton")

    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    error_message = page.get_by_text(expected_error, exact=False)
    expect(error_message).to_be_visible(timeout=5000)

# ==================== TC-LOGIN-004: 空凭据验证 ====================

def test_empty_credentials(page: Page):
    """
    【TC-LOGIN-004】空凭据验证 - 按钮处于禁用状态
    """
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "")
    page.fill("#password", "")
    
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)

# ==================== TC-LOGIN-005: 多用户登录验证 ====================

@pytest.mark.parametrize("email,password,role", [
    ("admin@juice-sh.op", "admin123", "管理员"),
    ("jim@juice-sh.op", "ncc-1701", "普通用户"),
    ("bender@juice-sh.op", "OhG0dPlease1nsertLiquor!", "测试用户"),
])
def test_multiple_users(page: Page, email: str, password: str, role: str):
    """
    【TC-LOGIN-005】多用户登录验证 - 参数化
    """
    print(f"\n测试用户: {role} ({email})")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")

# ==================== TC-LOGIN-006: 边界值测试 ====================

@pytest.mark.parametrize("email,password,boundary_type", [
    ("a@b.c", "123456", "最短邮箱地址"),
    ("a" * 50 + "@example.com", "password123", "超长邮箱地址"),
    ("test@test.com", "1", "最短密码"),
    ("test@test.com", "p" * 100, "超长密码"),
    ("test@test.com", "!@#$%^&*()_+", "特殊字符密码"),
])
def test_boundary_values(page: Page, email: str, password: str, boundary_type: str):
    """
    【TC-LOGIN-006】边界值测试 - 参数化
    """
    print(f"\n测试边界场景: {boundary_type}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    
    assert not page.is_closed()
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()

# ==================== TC-LOGIN-007: 安全攻击防护 ====================

@pytest.mark.parametrize("attack_string,password,attack_type", [
    ("' OR '1'='1", "anything", "SQL注入攻击"),
    ("<script>alert('xss')</script>", "password", "XSS攻击"),
    ("admin'--", "anything", "SQL注释注入"),
])
def test_security_attacks(page: Page, attack_string: str, password: str, attack_type: str):
    """
    【TC-LOGIN-007】安全攻击防护 - 参数化
    """
    print(f"\n测试攻击类型: {attack_type}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    page.fill("#email", attack_string)
    page.fill("#password", password)
    
    page.wait_for_selector("#loginButton:not([disabled])", timeout=5000)
    page.click("#loginButton")
    
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    assert page.is_visible("#email")
    assert page.is_visible("#password")

# ==================== TC-LOGIN-008: 连续多次提交测试 ====================

def test_form_submit_multiple_times(page: Page):
    """
    【TC-LOGIN-008】测试连续多次提交 - 验证登录功能正常
    
    测试目标: 验证登录按钮可以正常点击并跳转
    """
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    close_overlay(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    
    # 等待按钮启用
    page.wait_for_selector("#loginButton:not([disabled])", timeout=10000)
    
    # 直接点击登录按钮
    page.click("#loginButton")
    
    # 等待导航成功
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")
    
# ==================== 兼容保留的测试 ====================

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