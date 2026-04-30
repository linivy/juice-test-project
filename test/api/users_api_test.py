# test/api/users_api_test.py
"""用户 API 测试"""

import pytest
import allure


@allure.feature("API测试")
@allure.story("用户接口")
class TestUsersAPI:
    
    @allure.title("TC-API-003: 用户登录凭证验证")
    def test_login_credentials(self, api_client, api_config):
        # 正确凭证
        response = api_client.post("/rest/user/login", json={
            "email": api_config.test_user_email,
            "password": api_config.test_user_password
        })
        assert response.status_code == 200
        print("✅ 正确凭证登录成功")
        
        # 错误凭证
        response = api_client.post("/rest/user/login", json={
            "email": api_config.test_user_email,
            "password": "wrong_password"
        })
        assert response.status_code == 401
        print("✅ 错误凭证登录失败")