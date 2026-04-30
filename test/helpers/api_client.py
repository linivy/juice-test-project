# test/helpers/api_client.py
"""API 客户端封装 - 支持多环境配置"""

import requests
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class APIClientConfig:
    """API 客户端配置"""
    base_url: str
    timeout: int = 30
    verify_ssl: bool = False


class APIClient:
    """通用 API 客户端"""
    
    def __init__(self, config: APIClientConfig):
        self.config = config
        self.session = requests.Session()
        self.session.verify = config.verify_ssl
        self.session.timeout = config.timeout
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def set_auth_token(self, token: str):
        """设置认证 token"""
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    
    def set_basic_auth(self, username: str, password: str):
        """设置 Basic Auth"""
        self.session.auth = (username, password)
    
    def set_headers(self, headers: Dict[str, str]):
        """设置请求头"""
        self.session.headers.update(headers)
    
    def get(self, path: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """GET 请求"""
        url = f"{self.config.base_url}{path}"
        return self.session.get(url, params=params, **kwargs)
    
    def post(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """POST 请求"""
        url = f"{self.config.base_url}{path}"
        return self.session.post(url, data=data, json=json, **kwargs)
    
    def put(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """PUT 请求"""
        url = f"{self.config.base_url}{path}"
        return self.session.put(url, data=data, json=json, **kwargs)
    
    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        url = f"{self.config.base_url}{path}"
        return self.session.delete(url, **kwargs)
    
    def close(self):
        """关闭 session"""
        self.session.close()