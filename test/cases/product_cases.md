# 商品功能测试点

## 功能概述
用户浏览和购买商品

## 自动化覆盖情况
| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-PROD-001 | test_product_list.py | test_product_list_display | ✅ 已自动化 |
| TC-PROD-002 | test_product_list.py | test_product_card_fields | ✅ 已自动化 |
| TC-PROD-003 | test_product_list.py | test_product_add_to_basket | ✅ 已自动化 |

## 未自动化的测试点
- [ ] TC-PROD-004: 商品详情页显示
- [ ] TC-PROD-005: 修改购物车商品数量
- [ ] TC-PROD-006: 删除购物车商品
- [ ] TC-PROD-007: 购物车列表显示
- [ ] TC-PROD-008: 结算流程
- [ ] TC-PROD-009: 商品按价格排序
- [ ] TC-PROD-010: 商品按销量排序

## BDD 格式
### TC-PROD-001
Given 用户已登录
When 用户访问商品列表页
Then 显示商品卡片列表

### TC-PROD-002
Given 用户已登录
When 用户查看商品卡片
Then 显示商品名称、价格、添加按钮

### TC-PROD-003
Given 用户已登录
When 用户点击商品卡片的"添加"按钮
Then 购物车数量增加