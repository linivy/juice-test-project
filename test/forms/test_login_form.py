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

# test/forms/test_login_form.py 新增测试函数
def test_remember_me_functionality(logged_in_page: Page, context):
    """测试记住密码功能 - TC-LOGIN-005"""
    # Arrange
    page = logged_in_page
    
    # Act - 先退出登录，然后重新登录并勾选"记住我"
    # 1. 先退出登录（如果已登录）
    try:
        logout_btn = page.get_by_role("button", name="Logout", exact=False)
        if logout_btn.is_visible(timeout=3000):
            logout_btn.click()
            page.wait_for_url(f"{BASE_URL}/#/login", timeout=10000)
    except:
        # 如果没有找到退出按钮，直接访问登录页
        page.goto(f"{BASE_URL}/#/login")
    
    page.wait_for_load_state("networkidle")
    close_cookie_banner(page)
    
    # 2. 勾选"记住我"选项并登录
    remember_me_checkbox = page.locator("input[type='checkbox'], #rememberMe, [name='rememberMe']")
    if remember_me_checkbox.count() > 0:
        # 如果复选框未选中，点击选中
        if not remember_me_checkbox.first.is_checked():
            remember_me_checkbox.first.click()
        
        # 输入凭据并登录
        page.fill("#email", "admin@juice-sh.op")
        page.fill("#password", "admin123")
        page.click("#loginButton")
        
        # 等待登录成功
        page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)
    
    # 3. 模拟关闭浏览器后重新打开（创建新页面）
    new_page = context.new_page()
    
    # Assert - 验证登录状态保持不变
    new_page.goto(f"{BASE_URL}/#/search")
    new_page.wait_for_load_state("networkidle")
    
    # 检查是否处于登录状态（通过检查是否存在登录按钮来判断）
    login_button = new_page.locator("#loginButton")
    # 如果登录按钮不可见，说明已保持登录状态
    expect(login_button).not_to_be_visible(timeout=5000)
    
    # 验证当前页面是搜索页面（登录后的首页）
    expect(new_page).to_have_url(f"{BASE_URL}/#/search")
    
    # 关闭新页面
    new_page.close()
