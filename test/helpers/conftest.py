# test/api/conftest.py
"""API 测试专用 fixtures"""

import pytest
from test.helpers.api_client import APIClient, APIClientConfig
from test.config.environment import get_config


@pytest.fixture(scope="session")
def api_config():
    """获取 API 配置"""
    return get_config()


@pytest.fixture(scope="session")
def api_client(api_config):
    """创建 API 客户端"""
    client = APIClient(APIClientConfig(
        base_url=api_config.api_base_url,
        timeout=api_config.api_timeout
    ))
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(api_client, api_config):
    """获取认证 token（登录后）"""
    response = api_client.post("/api/login", json={
        "email": api_config.test_user_email,
        "password": api_config.test_user_password
    })
    assert response.status_code == 200
    return response.json().get("token")


@pytest.fixture(scope="session")
def authenticated_api_client(api_client, auth_token):
    """已认证的 API 客户端"""
    api_client.set_auth_token(auth_token)
    return api_client