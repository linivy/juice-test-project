# test/api/auth_api_test.py
"""认证 API 测试"""

import pytest
import allure


@allure.feature("API测试")
@allure.story("认证接口")
class TestAuthAPI:
    
    @allure.title("TC-API-001: 用户登录成功")
    def test_login_success(self, api_client, api_config):
        response = api_client.post("/rest/user/login", json={
            "email": api_config.test_user_email,
            "password": api_config.test_user_password
        })
        assert response.status_code == 200
        assert "authentication" in response.json()
        print("✅ 登录成功")
    
    @allure.title("TC-API-002: 用户登录失败")
    @pytest.mark.parametrize("email,password", [
        ("admin@juice-sh.op", "wrongpassword"),
        ("", "admin123"),
        ("admin@juice-sh.op", ""),
    ])
    def test_login_failed(self, api_client, email, password):
        response = api_client.post("/rest/user/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 401
        print("✅ 登录失败（符合预期）")