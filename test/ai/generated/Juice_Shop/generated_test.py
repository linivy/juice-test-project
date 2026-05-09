import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"

# 测试数据
test_data = [
    # ========== P0: 核心功能 ==========
    pytest.param("admin@juice-sh.op", "admin123", {"success": True}, id="TC-001-正常登录-管理员"),
    pytest.param("jim@juice-sh.op", "ncc-1701", {"success": True}, id="TC-002-正常登录-普通用户"),
    pytest.param("", "admin123", {"success": False, "error": "Email is required"}, id="TC-003-空邮箱"),
    pytest.param("admin@juice-sh.op", "", {"success": False, "error": "Password is required"}, id="TC-004-空密码"),
    pytest.param("wrong@user.com", "wrongpass", {"success": False, "error": "Invalid email or password"}, id="TC-005-无效凭据-邮箱错误"),
    pytest.param("admin@juice-sh.op", "wrongpass", {"success": False, "error": "Invalid email or password"}, id="TC-006-无效凭据-密码错误"),

    # ========== P1: 边界与安全 ==========
    pytest.param("test", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-007-邮箱格式校验-无@"),
    pytest.param("test@", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-008-邮箱格式校验-无域名"),
    pytest.param("' OR 1=1 --", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-009-SQL注入-邮箱"),
    pytest.param("admin@juice-sh.op", "' OR 1=1 --", {"success": False, "error": "Invalid email or password"}, id="TC-010-SQL注入-密码"),
    pytest.param("<script>alert(1)</script>", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-011-XSS攻击-邮箱"),
    pytest.param("admin@juice-sh.op", "<script>alert(1)</script>", {"success": False, "error": "Invalid email or password"}, id="TC-012-XSS攻击-密码"),

    # ========== P2: 体验与兼容 ==========
    pytest.param("Admin@juice-sh.op", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-013-大小写敏感-邮箱大写"),
    pytest.param("admin@juice-sh.op", "Admin123", {"success": False, "error": "Invalid email or password"}, id="TC-014-大小写敏感-密码大写"),
    pytest.param(" admin@juice-sh.op", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-015-前后空格-邮箱前空格"),
    pytest.param("admin@juice-sh.op ", "admin123", {"success": False, "error": "Invalid email or password"}, id="TC-016-前后空格-邮箱后空格"),
    pytest.param("admin@juice-sh.op", " admin123 ", {"success": False, "error": "Invalid email or password"}, id="TC-017-前后空格-密码前后空格"),
]

def close_cookie_banner(page: Page):
    """关闭Cookie横幅"""
    try:
        cookie_banner = page.locator("button[aria-label='Close Welcome Banner']")
        if cookie_banner.is_visible(timeout=3000):
            cookie_banner.click()
            page.wait_for_timeout(500)  # 等待横幅关闭动画
    except:
        pass

class TestLOGIN:
    """登录模块测试类"""
    
    @pytest.mark.parametrize("email,password,expected", test_data)
    def test_login(self, page: Page, email, password, expected):
        """测试登录功能"""
        # 1. 导航到登录页面
        page.goto(f"{BASE_URL}/#/login")
        page.wait_for_load_state("networkidle")
        
        # 2. 关闭Cookie横幅
        close_cookie_banner(page)
        
        # 3. 获取登录按钮
        login_button = page.locator("#loginButton")
        
        # 4. 处理空字段情况
        if not email or not password:
            # 如果邮箱为空，只填写密码
            if email:
                page.fill("#email", email)
            if password:
                page.fill("#password", password)
            
            # 验证登录按钮是否被禁用
            expect(login_button).to_be_disabled()
            return
        
        # 5. 填写表单
        page.fill("#email", email)
        page.fill("#password", password)
        
        # 6. 点击登录按钮
        login_button.click()
        page.wait_for_load_state("networkidle")
        
        # 7. 验证结果
        if expected.get("success"):
            # 成功登录：验证跳转到搜索页面
            expect(page).to_have_url(f"{BASE_URL}/#/search")
        else:
            # 失败登录：验证仍在登录页面
            expect(page).to_have_url(f"{BASE_URL}/#/login")
            
            # 验证错误消息
            error_msg = expected.get("error", "Invalid email or password")
            error_element = page.locator(f"text={error_msg}")
            expect(error_element).to_be_visible()