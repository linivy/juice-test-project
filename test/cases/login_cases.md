# 登录功能测试点

## P0 - 核心功能
- [ ] TC-LOGIN-001: 有效用户名密码，登录成功
- [ ] TC-LOGIN-002: 无效密码，登录失败
- [ ] TC-LOGIN-003: 空用户名/密码，登录失败

## BDD 格式
### TC-LOGIN-001
Given 用户打开登录页
When 用户输入 "admin@juice-sh.op" 和 "admin123"
Then 跳转到搜索页