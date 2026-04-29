# 登录功能测试点

## 自动化覆盖情况

| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-LOGIN-001 | test_login_form.py | test_login_page_loads | ✅ 已自动化 |
| TC-LOGIN-002 | test_login_form.py | test_login_with_valid_credentials | ✅ 已自动化 |
| TC-LOGIN-003 | test_login_form.py | test_login_with_invalid_credentials | ✅ 已自动化 |
| TC-LOGIN-004 | test_login_form.py | test_login_with_empty_credentials | ✅ 已自动化 |

## 已自动化测试点（BDD 格式）

### TC-LOGIN-001: 登录页面加载
Given 用户打开登录页面
When 页面加载完成
Then 显示邮箱输入框
And 显示密码输入框
And 显示登录按钮

### TC-LOGIN-002: 有效凭据登录
Given 用户打开登录页面
When 用户输入 "admin@juice-sh.op" 和 "admin123"
And 点击登录按钮
Then 跳转到搜索页面

### TC-LOGIN-003: 无效凭据登录
Given 用户打开登录页面
When 用户输入无效邮箱和密码
And 点击登录按钮
Then 显示错误提示
And 停留在登录页面

### TC-LOGIN-004: 空凭据登录
Given 用户打开登录页面
When 邮箱和密码为空
Then 登录按钮处于禁用状态

## 未自动化测试点（BDD 格式）

### TC-LOGIN-005: 记住密码功能
Given 用户已登录
When 用户勾选"记住我"选项
And 关闭浏览器后重新打开
Then 登录状态保持不变

### TC-LOGIN-006: 密码找回功能
Given 用户打开登录页面
When 用户点击"忘记密码"链接
Then 跳转到密码找回页面
And 显示邮箱输入框

### TC-LOGIN-007: 连续多次登录失败后账户锁定
Given 用户尝试登录
When 用户连续 5 次输入错误密码
Then 账户被临时锁定
And 显示"账户已锁定"提示

### TC-LOGIN-008: 注销功能
Given 用户已登录
When 用户点击注销按钮
Then 跳转到登录页面
And 需要重新输入密码才能访问