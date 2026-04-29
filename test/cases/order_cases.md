# 订单功能测试点

## 功能概述
用户查看和管理订单

## 自动化覆盖情况
| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-ORDER-001 | test_order_list.py | test_order_list_page_loads | ✅ 已自动化 |
| TC-ORDER-002 | test_order_list.py | test_order_list_displays_order_details | ✅ 已自动化 |
| TC-ORDER-003 | test_order_list.py | test_order_list_navigation_from_navbar | ✅ 已自动化 |
| TC-ORDER-004 | test_order_detail.py | test_order_detail_fields | ✅ 已自动化 |
| TC-ORDER-005 | test_order_detail.py | test_order_detail_back_button | ✅ 已自动化 |

## 未自动化的测试点
- [ ] TC-ORDER-006: 取消订单
- [ ] TC-ORDER-007: 重复下单同一商品
- [ ] TC-ORDER-008: 订单状态更新（待支付→已支付→已发货）
- [ ] TC-ORDER-009: 订单分页功能（多页时）
- [ ] TC-ORDER-010: 空订单状态的显示

## BDD 格式
### TC-ORDER-001
Given 用户已登录
When 用户访问订单列表页
Then 页面正常加载

### TC-ORDER-002
Given 用户已登录且有订单
When 用户访问订单列表页
Then 显示订单号、商品名称、数量、总价、状态

### TC-ORDER-004
Given 用户已登录且有订单
When 用户点击某个订单
Then 显示订单详情（订单号、商品、总价、状态）