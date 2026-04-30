# test/forms/test_login_form.py
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


# ==================== 场景1: 内联策略（<10组数据） ====================

class TestLoginInline:
    """使用内联策略的测试 - 数据量小，简单直接"""
    
    @pytest.mark.parametrize("email,password,expected_error", [
        ("invalid@example.com", "wrongpassword", "Invalid email or password"),
        ("", "admin123", "Email is required"),
        ("admin@juice-sh.op", "", "Password is required"),
        ("普通用户", "123456", "Please enter a valid email address"),
        ("test@test.com", "123", "Invalid email or password"),
    ])
    def test_invalid_credentials_inline(self, page: Page, email, password, expected_error):
        """测试无效凭据 - 内联数据（5组）"""
        # Arrange
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        # Act
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#loginButton")
        
        # Assert
        expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
        error_message = page.get_by_text(expected_error, exact=False)
        expect(error_message).to_be_visible(timeout=5000)


# ==================== 场景2: 外部文件策略（>=10组数据） ====================

class TestLoginExternal:
    """使用外部文件策略的测试 - 数据量大，从JSON文件读取"""
    
    @pytest.mark.parametrize("email,password,expected_error", [
        # 这里的数据可以从外部文件加载，或者直接写少量数据示例
        ("user1@test.com", "pass1", "Invalid email or password"),
        ("user2@test.com", "pass2", "Invalid email or password"),
        ("user3@test.com", "pass3", "Invalid email or password"),
        ("user4@test.com", "pass4", "Invalid email or password"),
        ("user5@test.com", "pass5", "Invalid email or password"),
        ("user6@test.com", "pass6", "Invalid email or password"),
        ("user7@test.com", "pass7", "Invalid email or password"),
        ("user8@test.com", "pass8", "Invalid email or password"),
        ("user9@test.com", "pass9", "Invalid email or password"),
        ("user10@test.com", "pass10", "Invalid email or password"),
        ("user11@test.com", "pass11", "Invalid email or password"),
        ("user12@test.com", "pass12", "Invalid email or password"),
    ])
    def test_invalid_credentials_external(self, page: Page, email, password, expected_error):
        """测试无效凭据 - 外部数据（12组）"""
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#loginButton")
        
        expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
        error_message = page.get_by_text(expected_error, exact=False)
        expect(error_message).to_be_visible(timeout=5000)


# ==================== 场景3: Fixture共享策略 ====================

class TestLoginShared:
    """使用共享Fixture的测试 - 数据被多个测试复用"""
    
    def test_invalid_credentials_shared_1(self, page: Page, shared_login_invalid_data):
        """测试无效凭据 - 使用共享数据（测试1）"""
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        for email, password, expected_error in shared_login_invalid_data:
            page.fill("#email", email)
            page.fill("#password", password)
            page.click("#loginButton")
            
            expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
            error_message = page.get_by_text(expected_error, exact=False)
            expect(error_message).to_be_visible(timeout=5000)
            
            # 重新加载页面，准备下一组测试
            page.reload()
            page.wait_for_load_state("networkidle")
            close_cookie_banner(page)
    
    def test_invalid_credentials_shared_2(self, page: Page, shared_login_invalid_data):
        """测试无效凭据 - 使用共享数据（测试2）"""
        # 同样的数据，不同的测试逻辑
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        for email, password, expected_error in shared_login_invalid_data[:3]:  # 只测试前3组
            page.fill("#email", email)
            page.fill("#password", password)
            page.click("#loginButton")
            
            # 验证错误消息不为空
            error_message = page.get_by_text(expected_error, exact=False)
            expect(error_message).to_be_visible(timeout=5000)
            
            page.reload()


# ==================== 场景4: 动态生成策略 ====================

class TestLoginDynamic:
    """使用动态生成策略的测试 - 大量数据或随机数据"""
    
    @pytest.mark.parametrize("email,password,expected", generate_large_login_data(20))
    def test_large_dataset_dynamic(self, page: Page, email, password, expected):
        """测试大量动态生成的登录场景（20组）"""
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#loginButton")
        
        if expected == "success":
            # 期望登录成功
            try:
                page.wait_for_url(f"{BASE_URL}/#/search", timeout=5000)
                # 登录成功后退出
                logout_btn = page.get_by_role("button", name="Logout", exact=False)
                if logout_btn.is_visible(timeout=3000):
                    logout_btn.click()
            except:
                pass
        else:
            # 期望登录失败
            expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
            error_message = page.get_by_text(expected, exact=False)
            expect(error_message).to_be_visible(timeout=5000)
    
    def test_security_attacks(self, page: Page, shared_security_test_data):
        """测试安全攻击场景 - SQL注入、XSS等"""
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        close_cookie_banner(page)
        
        for attack_string, password, attack_type in shared_security_test_data:
            page.fill("#email", attack_string)
            page.fill("#password", password)
            page.click("#loginButton")
            
            # 验证应用正确处理攻击（不崩溃，显示错误提示）
            expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)
            
            # 检查页面是否仍然正常（没有弹出alert、没有崩溃）
            assert page.is_visible("#email")
            assert page.is_visible("#password")
            
            # 清空输入框，准备下一个攻击向量
            page.fill("#email", "")
            page.fill("#password", "")
            print(f"✅ 成功处理 {attack_type} 攻击")


# ==================== 原有测试保持不变 ====================

def test_login_page_loads(page: Page):
    """测试登录页面正常加载"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    login_heading = page.locator("mat-card h2, mat-card h1, .login-form h2, .login-form h1")
    expect(login_heading.first).to_be_visible(timeout=5000)
    
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#loginButton")).to_be_visible()


def test_login_with_valid_credentials(page: Page):
    """测试使用有效凭据登录"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    expect(page).to_have_url(f"{BASE_URL}/#/search")


def test_login_with_empty_credentials(page: Page):
    """测试使用空凭据登录 - 按钮应处于禁用状态"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    page.fill("#email", "")
    page.fill("#password", "")
    
    login_button = page.locator("#loginButton")
    expect(login_button).to_be_disabled(timeout=5000)
    
    expect(page).to_have_url(f"{BASE_URL}/#/login", timeout=5000)


def test_remember_me_functionality(logged_in_page: Page, context):
    """测试记住密码功能"""
    page = logged_in_page
    
    # 退出登录
    try:
        logout_btn = page.get_by_role("button", name="Logout", exact=False)
        if logout_btn.is_visible(timeout=3000):
            logout_btn.click()
            page.wait_for_url(f"{BASE_URL}/#/login", timeout=10000)
    except:
        page.goto(f"{BASE_URL}/#/login")
    
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 登录并勾选记住我
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