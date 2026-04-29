# 商品功能测试点

## 自动化覆盖情况

| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-PROD-001 | test_product_list.py | test_product_list_display | ✅ 已自动化 |
| TC-PROD-002 | test_product_list.py | test_product_card_fields | ✅ 已自动化 |
| TC-PROD-003 | test_product_list.py | test_product_add_to_basket | ✅ 已自动化 |
| TC-PROD-004 | test_product_list.py | test_product_list_search | ✅ 已自动化 |

## 已自动化测试点（BDD 格式）

### TC-PROD-001: 商品列表显示
Given 用户已登录
When 用户访问商品列表页
Then 显示商品卡片
And 至少有一个商品

### TC-PROD-002: 商品卡片字段验证
Given 用户已登录
When 用户查看商品卡片
Then 卡片内容不为空
And 显示价格信息

### TC-PROD-003: 添加商品到购物车
Given 用户已登录
When 用户点击商品的 "Add to Basket" 按钮
Then 购物车数量增加

### TC-PROD-004: 商品列表内搜索
Given 用户已登录
When 用户在搜索框输入 "Apple" 并搜索
Then 搜索结果包含 "Apple"

## 未自动化测试点（BDD 格式）

### TC-PROD-005: 商品详情页显示
Given 用户已登录
When 用户点击商品卡片
Then 跳转到商品详情页
And 显示商品名称、价格、描述、图片

### TC-PROD-006: 修改购物车商品数量
Given 用户已登录
And 购物车中有商品
When 用户修改商品数量
Then 总价相应变化
And 购物车数量更新

### TC-PROD-007: 删除购物车商品
Given 用户已登录
And 购物车中有商品
When 用户点击删除按钮
Then 商品从购物车移除
And 总价减少

### TC-PROD-008: 购物车列表显示
Given 用户已登录
And 购物车中有多个商品
When 用户打开购物车页面
Then 显示所有商品
And 显示每个商品的价格和数量
And 显示总价

### TC-PROD-009: 结算流程
Given 用户已登录
And 购物车中有商品
When 用户点击结算按钮
Then 进入结算页面
And 要求填写收货地址和支付方式
And 确认后生成订单

### TC-PROD-010: 商品按价格排序
Given 用户已登录
When 用户点击"按价格排序"
Then 商品列表按价格升序排列
And 再次点击按价格降序排列

### TC-PROD-011: 商品按销量排序
Given 用户已登录
When 用户点击"按销量排序"
Then 商品列表按销量降序排列