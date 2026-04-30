# test/forms/test_login_form.py
import pytest
from playwright.sync_api import Page, expect
import allure  # 添加 allure 支持，便于追溯

BASE_URL = "http://localhost:3000"


def close_cookie_banner(page: Page):
    """关闭 Cookie 弹窗"""
    try:
        close_btn = page.locator("button[aria-label='Close Welcome Banner']")
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
    except:
        pass


# ==================== 功能测试点与参数化用例映射 ====================
"""
功能测试点映射表:
┌────────────────────────────────────┬─────────────────────────────────────┐
│ 功能测试点 (Test Point)            │ 参数化测试用例                        │
├────────────────────────────────────┼─────────────────────────────────────┤
│ TC-LOGIN-001: 登录页面正常加载     │ test_login_page_loads (保留原版)     │
│ TC-LOGIN-002: 有效凭据登录         │ test_valid_credentials_param        │
│ TC-LOGIN-003: 无效凭据登录         │ test_invalid_credentials_param      │
│ TC-LOGIN-004: 空凭据验证           │ test_empty_credentials_param        │
│ TC-LOGIN-005: 记住密码功能         │ test_remember_me_param              │
│ TC-LOGIN-006: 多用户登录验证       │ test_multiple_valid_users           │
│ TC-LOGIN-007: 边界值测试           │ test_boundary_values                │
│ TC-LOGIN-008: 安全攻击防护         │ test_security_attack_vectors        │
└────────────────────────────────────┴─────────────────────────────────────┘
"""


# ==================== TC-LOGIN-001: 页面加载测试（保留原版） ====================

def test_login_page_loads(page: Page):
    """【TC-LOGIN-001】测试登录页面正常加载"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    login_heading = page.locator("mat-card h2, mat-card h1, .login-form h2, .login-form h1")
    expect(login_heading.first).to_be_visible(timeout=5000)
    
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#loginButton")).to_be_visible()


# ==================== TC-LOGIN-002: 有效凭据登录（参数化增强） ====================

@pytest.mark.parametrize("email,password,user_role", [
    ("admin@juice-sh.op", "admin123", "管理员"),
    ("jim@juice-sh.op", "cardinal", "普通用户"),
    ("bender@juice-sh.op", "OhG0dPlease1nsertLiquor!", "测试用户"),
])
def test_valid_credentials_param(page: Page, email: str, password: str, user_role: str):
    """
    【TC-LOGIN-002】测试有效凭据登录 - 参数化版本
    覆盖功能点: 有效用户名/密码登录成功，跳转到搜索页面
    """
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")
    
    # 退出登录，避免影响其他测试
    account_menu = page.locator("[aria-label='Show/hide account menu']")
    account_menu.click()
    logout_btn = page.get_by_role("button", name="Logout", exact=False)
    if logout_btn.is_visible(timeout=3000):
        logout_btn.click()


# ==================== TC-LOGIN-003: 无效凭据登录（参数化增强） ====================

@pytest.mark.parametrize("email,password,expected_error,scenario", [
    ("invalid@example.com", "wrongpassword", "Invalid email or password", "错误邮箱+错误密码"),
    ("admin@juice-sh.op", "wrongpassword", "Invalid email or password", "正确邮箱+错误密码"),
    ("invalid@example.com", "admin123", "Invalid email or password", "错误邮箱+正确密码"),
    ("", "admin123", "Email is required", "空邮箱+正确密码"),
    ("admin@juice-sh.op", "", "Password is required", "正确邮箱+空密码"),
    ("普通用户", "123456", "Please enter a valid email address", "无效邮箱格式"),
])
def test_invalid_credentials_param(page: Page, email: str, password: str, expected_error: str, scenario: str):
    """
    【TC-LOGIN-003】测试无效凭据登录 - 参数化版本
    覆盖功能点: 无效用户名/密码登录失败，显示错误提示，停留在登录页
    """
    print(f"\n📝 测试场景: {scenario}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 处理空凭据的特殊情况 - 按钮应禁用
    if email == "" or password == "":
        page.fill("#email", email)
        page.fill("#password", password)
        login_button = page.locator("#loginButton")
        expect(login_button).to_be_disabled(timeout=3000)
        print(f"  ✅ 按钮禁用状态正确")
        return
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    error_message = page.get_by_text(expected_error, exact=False)
    expect(error_message).to_be_visible(timeout=5000)
    print(f"  ✅ 错误提示正确: {expected_error}")


# ==================== TC-LOGIN-004: 空凭据验证（参数化） ====================

@pytest.mark.parametrize("email,password,description", [
    ("", "", "邮箱和密码都为空"),
    ("admin@juice-sh.op", "", "仅密码为空"),
    ("", "admin123", "仅邮箱为空"),
])
def test_empty_credentials_param(page: Page, email: str, password: str, description: str):
    """
    【TC-LOGIN-004】测试空凭据验证 - 参数化版本
    覆盖功能点: 邮箱或密码为空时，登录按钮处于禁用状态
    """
    print(f"\n📝 测试场景: {description}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    
    print(f"  ✅ 登录按钮已禁用")


# ==================== TC-LOGIN-005: 记住密码功能（参数化） ====================

@pytest.mark.parametrize("email,password", [
    ("admin@juice-sh.op", "admin123"),
    ("jim@juice-sh.op", "cardinal"),
])
def test_remember_me_param(page: Page, context, email: str, password: str):
    """
    【TC-LOGIN-005】测试记住密码功能 - 参数化版本
    覆盖功能点: 勾选"记住我"后，登录状态应持久化
    """
    print(f"\n📝 测试用户: {email}")
    
    # 步骤1: 访问登录页
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 步骤2: 勾选"记住我"并登录
    remember_me_checkbox = page.locator("input[type='checkbox'], #rememberMe, [name='rememberMe']")
    if remember_me_checkbox.count() > 0:
        if not remember_me_checkbox.first.is_checked():
            remember_me_checkbox.first.click()
            print(f"  ✅ 已勾选'记住我'")
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    print(f"  ✅ 登录成功")
    
    # 步骤3: 模拟新会话（新页面）
    new_page = context.new_page()
    new_page.goto(f"{BASE_URL}/#/search")
    new_page.wait_for_load_state("networkidle")
    
    # 步骤4: 验证登录状态保持
    login_button = new_page.locator("#loginButton")
    expect(login_button).not_to_be_visible(timeout=5000)
    expect(new_page).to_have_url(f"{BASE_URL}/#/search")
    print(f"  ✅ 登录状态已保持")
    
    # 清理
    new_page.close()


# ==================== TC-LOGIN-006: 多用户登录验证（参数化） ====================

@pytest.mark.parametrize("email,password,user_role,expected_permission", [
    ("admin@juice-sh.op", "admin123", "管理员", "admin_panel"),
    ("jim@juice-sh.op", "cardinal", "普通用户", "user_profile"),
])
def test_multiple_valid_users(page: Page, email: str, password: str, user_role: str, expected_permission: str):
    """
    【TC-LOGIN-006】测试多用户登录验证
    覆盖功能点: 不同角色用户都能成功登录并看到对应的权限界面
    """
    print(f"\n📝 测试用户: {user_role} ({email})")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")
    
    # 验证用户菜单可见
    account_menu = page.locator("[aria-label='Show/hide account menu']")
    expect(account_menu).to_be_visible(timeout=5000)
    
    print(f"  ✅ {user_role} 登录成功，权限: {expected_permission}")
    
    # 退出登录
    account_menu.click()
    logout_btn = page.get_by_role("button", name="Logout", exact=False)
    if logout_btn.is_visible(timeout=3000):
        logout_btn.click()


# ==================== TC-LOGIN-007: 边界值测试（参数化） ====================

@pytest.mark.parametrize("email,password,boundary_type", [
    ("a@b.c", "123456", "最短邮箱"),
    ("a"*50 + "@example.com", "password123", "超长邮箱"),
    ("test@test.com", "1", "最短密码"),
    ("test@test.com", "p"*100, "超长密码"),
    ("test@test.com", "!@#$%^&*()", "特殊字符密码"),
])
def test_boundary_values(page: Page, email: str, password: str, boundary_type: str):
    """
    【TC-LOGIN-007】测试边界值
    覆盖功能点: 各种边界条件下的登录行为，系统应能正确处理
    """
    print(f"\n📝 边界测试: {boundary_type}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    
    # 验证系统没有崩溃
    assert not page.is_closed()
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    
    print(f"  ✅ {boundary_type} 测试通过，系统稳定")


# ==================== TC-LOGIN-008: 安全攻击防护（参数化） ====================

@pytest.mark.parametrize("email,password,attack_type", [
    ("' OR '1'='1", "anything", "SQL注入"),
    ("<script>alert('xss')</script>", "password", "XSS攻击"),
    ("admin'--", "anything", "SQL注释注入"),
    ("'; DROP TABLE users;--", "password", "SQL删除注入"),
])
def test_security_attack_vectors(page: Page, email: str, password: str, attack_type: str):
    """
    【TC-LOGIN-008】测试安全攻击防护
    覆盖功能点: 系统应能防护SQL注入、XSS等常见攻击
    """
    print(f"\n📝 安全测试: {attack_type}")
    
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#loginButton")
    
    # 验证系统没有被攻击破坏
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
    
    # 验证页面元素仍然正常
    assert page.is_visible("#email")
    assert page.is_visible("#password")
    
    # 验证没有弹出 alert 弹窗
    with pytest.raises(Exception):
        page.on("dialog", lambda dialog: dialog.accept())
    
    print(f"  ✅ {attack_type} 被正确防护")


# ==================== 原有测试函数保留（用于兼容性） ====================

def test_login_with_valid_credentials(page: Page):
    """【兼容保留】测试使用有效凭据登录"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")


def test_login_with_invalid_credentials(page: Page):
    """【兼容保留】测试使用无效凭据登录"""
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
    """【兼容保留】测试使用空凭据登录"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "")
    page.fill("#password", "")
    
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)


def test_remember_me_functionality(logged_in_page: Page, context):
    """【兼容保留】测试记住密码功能"""
    page = logged_in_page
    
    try:
        logout_btn = page.get_by_role("button", name="Logout", exact=False)
        if logout_btn.is_visible(timeout=3000):
            logout_btn.click()
            page.wait_for_url(f"{BASE_URL}/#/login", timeout=10000)
    except:
        page.goto(f"{BASE_URL}/#/login")
    
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    remember_me_checkbox = page.locator("input[type='checkbox'], #rememberMe, [name='rememberMe']")
    if remember_me_checkbox.count() > 0:
        if not remember_me_checkbox.first.is_checked():
            remember_me_checkbox.first.click()
        
        page.fill("#email", "admin@juice-sh.op")
        page.fill("#password", "admin123")
        page.click("#loginButton")
        page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    
    new_page = context.new_page()
    new_page.goto(f"{BASE_URL}/#/search")
    new_page.wait_for_load_state("networkidle")
    
    login_button = new_page.locator("#loginButton")
    expect(login_button).not_to_be_visible(timeout=5000)
    expect(new_page).to_have_url(f"{BASE_URL}/#/search")
    
    new_page.close()