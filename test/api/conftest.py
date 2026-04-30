# test/api/conftest.py
"""API 测试专用 fixtures"""

import pytest
import sys
import os

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from test.helpers.api_client import APIClient, APIClientConfig
from test.config.environment import get_config


@pytest.fixture(scope="session")
def api_config():
    return get_config()


@pytest.fixture(scope="session")
def api_client(api_config):
    client = APIClient(APIClientConfig(
        base_url=api_config.api_base_url,
        timeout=api_config.api_timeout
    ))
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(api_client, api_config):
    response = api_client.post("/rest/user/login", json={
        "email": api_config.test_user_email,
        "password": api_config.test_user_password
    })
    if response.status_code == 200:
        data = response.json()
        return data.get("authentication", {}).get("token")
    return None


@pytest.fixture(scope="session")
def authenticated_api_client(api_client, auth_token):
    if auth_token:
        api_client.set_auth_token(auth_token)
    return api_client