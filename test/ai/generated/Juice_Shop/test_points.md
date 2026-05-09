好的，作为资深测试架构师，我将基于你提供的 Juice Shop 项目信息和需求，为你输出 Login 模块的测试设计。

---

### 一、功能测试点

| 优先级 | 测试点 | 描述 |
| :--- | :--- | :--- |
| **P0** | **正常登录（管理员）** | 使用管理员账号 `admin@juice-sh.op` / `admin123` 登录，验证成功跳转到 `/#/search`。 |
| **P0** | **正常登录（普通用户）** | 使用普通用户账号 `jim@juice-sh.op` / `ncc-1701` 登录，验证成功跳转到 `/#/search`。 |
| **P0** | **空邮箱** | 不输入邮箱，输入密码，点击登录，验证显示错误消息 `Email is required`。 |
| **P0** | **空密码** | 输入邮箱，不输入密码，点击登录，验证显示错误消息 `Password is required`。 |
| **P0** | **无效凭据** | 输入不存在的邮箱或错误的密码，验证显示错误消息 `Invalid email or password`。 |
| **P1** | **邮箱格式校验** | 输入不符合邮箱格式的字符串（如 `test`、`test@`），验证前端或后端是否给出合理提示。 |
| **P1** | **密码长度/复杂度** | 输入极短或极长的密码，验证系统是否有限制或给出提示。 |
| **P1** | **SQL注入尝试** | 在邮箱或密码字段输入 SQL 注入 payload（如 `' OR 1=1 --`），验证登录失败且无异常。 |
| **P1** | **XSS攻击尝试** | 在邮箱或密码字段输入 XSS payload（如 `<script>alert(1)</script>`），验证 payload 被转义或拒绝。 |
| **P2** | **大小写敏感** | 使用 `Admin@juice-sh.op` 或 `ADMIN@JUICE-SH.OP` 登录，验证是否区分大小写。 |
| **P2** | **前后空格处理** | 在邮箱或密码前后添加空格（如 ` admin@juice-sh.op `），验证系统是否自动 trim。 |
| **P2** | **连续快速点击** | 快速连续点击登录按钮多次，验证是否只发送一次请求或正确处理。 |
| **P2** | **页面刷新后状态** | 登录成功后刷新页面，验证用户会话是否保持（即仍处于登录状态）。 |

---

### 二、参数化测试数据

```python
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
    pytest.param(" admin@juice-sh.op", "admin123", {"success": True}, id="TC-015-前后空格-邮箱前空格"),
    pytest.param("admin@juice-sh.op ", "admin123", {"success": True}, id="TC-016-前后空格-邮箱后空格"),
    pytest.param("admin@juice-sh.op", " admin123 ", {"success": False, "error": "Invalid email or password"}, id="TC-017-前后空格-密码前后空格"),
]
```

**说明：**
1.  **`success: True`**：表示期望登录成功，最终断言应验证 URL 跳转到 `/#/search`。
2.  **`success: False`**：表示期望登录失败，最终断言应验证页面显示对应的 `error` 消息。
3.  测试数据覆盖了 P0 核心流程、P1 安全边界和 P2 用户体验场景，便于 pytest 直接参数化执行。