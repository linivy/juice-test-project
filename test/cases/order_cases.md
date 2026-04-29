# 订单功能测试点

## 自动化覆盖情况

| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-ORDER-001 | test_order_list.py | test_order_list_page_loads | ✅ 已自动化 |
| TC-ORDER-002 | test_order_list.py | test_order_list_displays_order_details | ✅ 已自动化 |
| TC-ORDER-003 | test_order_list.py | test_order_list_navigation_from_navbar | ✅ 已自动化 |
| TC-ORDER-004 | test_order_detail.py | test_order_detail_fields | ✅ 已自动化 |
| TC-ORDER-005 | test_order_detail.py | test_order_detail_back_button | ✅ 已自动化 |

## 已自动化测试点（BDD 格式）

### TC-ORDER-001: 订单列表页加载
Given 用户已登录
When 用户访问订单列表页
Then 页面正常加载
And URL 包含 "/#/orders"

### TC-ORDER-002: 订单列表详情显示
Given 用户已登录且有订单
When 用户访问订单列表页
Then 显示订单号（包含 # 符号）
And 显示商品名称（如 Apple）
And 显示数量（数字）
And 显示总价（包含货币符号）
And 显示订单状态

### TC-ORDER-003: 导航栏访问订单列表
Given 用户已登录
When 用户点击导航栏的 "Orders" 链接
Then 跳转到订单列表页
And URL 包含 "/#/orders"

### TC-ORDER-004: 订单详情字段验证
Given 用户已登录且有订单
When 用户点击某个订单进入详情页
Then 显示订单号
And 显示商品名称
And 显示总价
And 显示订单状态

### TC-ORDER-005: 订单详情返回按钮
Given 用户在订单详情页
When 用户点击返回按钮
Then 返回订单列表页

## 未自动化测试点（BDD 格式）

### TC-ORDER-006: 取消订单
Given 用户已登录且有未完成的订单
When 用户在订单列表页点击"取消订单"
And 确认取消操作
Then 订单状态变为"已取消"

### TC-ORDER-007: 重复下单同一商品
Given 用户已登录
When 用户对同一商品重复下单
Then 订单列表中出现多个相同商品的订单
And 每个订单独立显示

### TC-ORDER-008: 订单状态更新
Given 用户有"待支付"状态的订单
When 用户完成支付
Then 订单状态更新为"已支付"
And 状态变化在订单列表中可见

### TC-ORDER-009: 订单分页功能
Given 用户有超过 10 个订单
When 用户访问订单列表页
Then 只显示前 10 个订单
And 有分页控件
And 点击下一页显示更多订单

### TC-ORDER-010: 空订单状态的显示
Given 用户已登录且没有任何订单
When 用户访问订单列表页
Then 显示空状态提示
And 提示"暂无订单"或类似信息