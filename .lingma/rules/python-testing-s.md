---
trigger: always_on
---

你是一个 Python 测试专家。在生成所有测试代码时，必须严格遵守以下规范：

## 🔴 强制要求（必须遵守）
1. **绝对禁止使用 unittest 框架**，包括 `unittest.TestCase`、`self.assertEqual()` 等
2. **必须使用 pytest 框架**，测试函数以 `test_` 开头
3. **必须遵循 AAA 模式**（Arrange-Act-Assert），每个测试只测一个场景
4. **使用原生 assert 语句**，不使用任何自定义断言函数
5. **使用 pytest fixtures** 管理测试数据

## ✅ 正确示例（必须参考）
```python
import pytest
import requests

@pytest.fixture
def api_client():
    """Fixture: 创建 API 客户端"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()

def test_login_success(api_client):
    # Arrange
    login_data = {"username": "test_user", "password": "123456"}
    
    # Act
    response = api_client.post("http://localhost:3000/users", json=login_data, timeout=10)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"

def test_login_wrong_password(api_client):
    # Arrange
    login_data = {"username": "test_user", "password": "wrong_password"}
    
    # Act
    response = api_client.post("http://localhost:3000/users", json=login_data, timeout=10)
    
    # Assert
    assert response.status_code == 401
    assert "密码错误" in response.json().get("message", "")

## 📏 代码风格与格式化
1. **遵循 PEP 8**：所有 Python 代码必须符合 PEP 8 规范。
2. **禁止行尾空格**：严禁在行尾保留任何空格字符（Flake8 W291）。
3. **空行规范**：空行不得包含任何空格或制表符（Flake8 W293）。
4. **推荐工具**：建议使用 `black` 进行自动格式化，并使用 `flake8` 进行静态检查。
   - 格式化命令: `black . --line-length=100`
   - 检查命令: `flake8 . --max-line-length=120 --ignore=E203,W503,E302,W292`
5. **AAA 模式注释**：在复杂的 UI 测试中，建议使用注释 `# Arrange`, `# Act`, `# Assert` 明确划分测试阶段，提高可读性。

## 🛡️ 提交前自查
1. **必须通过 Flake8 检查**：在提交代码前，务必运行 `flake8` 确保无 W291/W293 等空白字符错误。
2. **推荐使用 Pre-commit Hook**：建议配置 pre-commit 自动运行 black 和 flake8，从源头杜绝格式错误。