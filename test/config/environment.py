# test/config/environment.py
"""多环境配置管理"""

import os
import pytest  # 添加这行导入
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Environment(Enum):
    """环境枚举"""
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    LOCAL = "local"


@dataclass
class AppConfig:
    """应用配置"""
    # 基础配置
    env: Environment
    base_url: str
    api_base_url: str
    
    # 数据库配置（可选）
    db_host: Optional[str] = None
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    
    # 测试用户
    test_user_email: str = "admin@juice-sh.op"
    test_user_password: str = "admin123"
    
    # 超时配置
    api_timeout: int = 30
    page_timeout: int = 30000
    
    # 其他配置
    headless: bool = True
    retry_times: int = 3


# 环境配置映射
ENV_CONFIGS = {
    Environment.LOCAL: AppConfig(
        env=Environment.LOCAL,
        base_url="http://localhost:3000",
        api_base_url="http://localhost:3000",
        db_host="localhost",
    ),
    Environment.DEV: AppConfig(
        env=Environment.DEV,
        base_url="https://dev.example.com",
        api_base_url="https://dev-api.example.com",
        test_user_email="test@dev.com",
        test_user_password="dev123",
        headless=True,
    ),
    Environment.STAGING: AppConfig(
        env=Environment.STAGING,
        base_url="https://staging.example.com",
        api_base_url="https://staging-api.example.com",
        test_user_email="test@staging.com",
        test_user_password="staging123",
        headless=True,
    ),
    Environment.PRODUCTION: AppConfig(
        env=Environment.PRODUCTION,
        base_url="https://example.com",
        api_base_url="https://api.example.com",
        test_user_email="",
        test_user_password="",
        headless=True,
        retry_times=5,
    ),
}


def get_config(env_name: Optional[str] = None) -> AppConfig:
    """
    获取环境配置
    
    优先级：
    1. 命令行参数 --env
    2. 环境变量 TEST_ENV
    3. 默认 local
    """
    # 获取环境名称
    if env_name is None:
        env_name = os.environ.get("TEST_ENV", "local")
    
    # 转换为枚举
    try:
        env = Environment(env_name.lower())
    except ValueError:
        print(f"⚠️ 未知环境: {env_name}, 使用 local")
        env = Environment.LOCAL
    
    return ENV_CONFIGS[env]


# 支持命令行参数
def pytest_addoption(parser):
    """添加 --env 命令行参数"""
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="选择测试环境: local, dev, staging, prod"
    )


@pytest.fixture(scope="session")
def env_config(request):
    """pytest fixture 获取环境配置"""
    env_name = request.config.getoption("--env")
    return get_config(env_name)