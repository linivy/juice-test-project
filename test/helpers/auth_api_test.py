# test/api/auth_api_test.py
"""认证 API 测试"""

import pytest
import allure


@allure.feature("API测试")
@allure.story("认证接口")
class TestAuthAPI:
    
    @allure.title("TC-API-001: 用户登录成功")
    def test_login_success(self, api_client, api_config):
        """测试用户登录成功"""
        response = api_client.post("/api/login", json={
            "email": api_config.test_user_email,
            "password": api_config.test_user_password
        })
        
        assert response.status_code == 200
        assert "token" in response.json()
        assert response.json().get("user", {}).get("email") == api_config.test_user_email
    
    @allure.title("TC-API-002: 用户登录失败 - 错误密码")
    @pytest.mark.parametrize("email,password,expected_error", [
        ("admin@juice-sh.op", "wrongpassword", "Invalid email or password"),
        ("", "admin123", "Email is required"),
        ("admin@juice-sh.op", "", "Password is required"),
    ])
    def test_login_failed(self, api_client, email, password, expected_error):
        """测试登录失败场景"""
        response = api_client.post("/api/login", json={
            "email": email,
            "password": password
        })
        
        assert response.status_code == 401
        assert expected_error in response.json().get("error", "")
    
    @allure.title("TC-API-003: 获取当前用户信息")
    def test_get_current_user(self, authenticated_api_client):
        """测试获取当前用户信息"""
        response = authenticated_api_client.get("/api/user")
        
        assert response.status_code == 200
        assert "email" in response.json()