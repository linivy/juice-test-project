# 登录功能测试点

## 功能概述
用户通过邮箱和密码登录系统

## 自动化覆盖情况
| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-LOGIN-001 | test_login_form.py | test_login_page_loads | ✅ 已自动化 |
| TC-LOGIN-002 | test_login_form.py | test_login_with_valid_credentials | ✅ 已自动化 |
| TC-LOGIN-003 | test_login_form.py | test_login_with_invalid_credentials | ✅ 已自动化 |
| TC-LOGIN-004 | test_login_form.py | test_login_with_empty_credentials | ✅ 已自动化 |

## 未自动化的测试点
- [ ] TC-LOGIN-005: 记住密码功能
- [ ] TC-LOGIN-006: 密码找回功能
- [ ] TC-LOGIN-007: 连续多次登录失败后账户锁定
- [ ] TC-LOGIN-008: 注销功能

## BDD 格式
### TC-LOGIN-001
Given 用户打开登录页
When 页面加载完成
Then 显示邮箱输入框、密码输入框、登录按钮

### TC-LOGIN-002
Given 用户打开登录页
When 用户输入 "admin@juice-sh.op" 和 "admin123"
Then 跳转到搜索页

### TC-LOGIN-003
Given 用户打开登录页
When 用户输入无效邮箱和密码
Then 显示错误提示，停留在登录页