---
name: api-testing-skill
description: API 自动化测试专家，使用 pytest + requests
trigger: manual
type: skill
---

# API 测试专家技能

## 核心能力

- 使用 `pytest` + `requests` 编写 API 测试
- 使用 `unittest.mock` 模拟外部依赖
- 使用 `@pytest.mark.parametrize` 进行参数化测试

## 测试模板

### 基础 API 测试
```python
import pytest
import requests

def test_api_endpoint():
    """测试 API 端点"""
    # Arrange
    url = "http://localhost:3000/api/endpoint"
    payload = {"key": "value"}
    
    # Act
    response = requests.post(url, json=payload, timeout=10)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True