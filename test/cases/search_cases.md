# 搜索功能测试点

## 自动化覆盖情况

| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-SEARCH-001 | test_search.py | test_search_exact_match | ✅ 已自动化 |
| TC-SEARCH-002 | test_search.py | test_search_partial_match | ✅ 已自动化 |
| TC-SEARCH-003 | test_search.py | test_search_no_match | ✅ 已自动化 |
| TC-SEARCH-004 | test_search.py | test_search_empty_string | ✅ 已自动化 |
| TC-SEARCH-005 | test_product_list.py | test_product_list_search | ✅ 已自动化 |

## 已自动化测试点（BDD 格式）

### TC-SEARCH-001: 精确匹配搜索
Given 用户已登录
When 用户输入 "Apple Juice" 并搜索
Then 搜索结果中显示 "Apple Juice"

### TC-SEARCH-002: 部分匹配搜索
Given 用户已登录
When 用户输入 "Apple" 并搜索
Then 搜索结果中显示所有包含 "Apple" 的商品
And 至少有一个结果

### TC-SEARCH-003: 无结果搜索
Given 用户已登录
When 用户输入 "NonExistentProductXYZ123" 并搜索
Then 显示 "No results found"
And 显示 "Try adjusting your search" 提示

### TC-SEARCH-004: 空字符串搜索
Given 用户已登录
And 用户已有搜索结果
When 用户清空搜索框并搜索
Then 显示所有商品
And 商品数量大于 0

### TC-SEARCH-005: 商品列表内搜索
Given 用户已登录
And 用户在商品列表页面
When 用户在搜索框输入 "Apple" 并搜索
Then 搜索结果包含 "Apple"

## 未自动化测试点（BDD 格式）

### TC-SEARCH-006: 搜索后点击搜索结果跳转详情
Given 用户已登录
When 用户搜索 "Apple Juice"
And 点击搜索结果中的商品
Then 跳转到商品详情页

### TC-SEARCH-007: 搜索历史记录
Given 用户已登录
When 用户多次搜索不同关键词
Then 搜索框下拉显示历史记录
And 点击历史记录可再次搜索

### TC-SEARCH-008: 热门搜索词推荐
Given 用户打开搜索页面
Then 搜索框下方显示热门搜索词
And 点击热门词可自动搜索

### TC-SEARCH-009: 搜索建议下拉框
Given 用户已登录
When 用户在搜索框输入 "Ap"
Then 下拉显示包含 "Ap" 的建议词
And 点击建议词可快速填充

### TC-SEARCH-010: 中英文混合搜索
Given 用户已登录
When 用户输入 "Apple 果汁" 并搜索
Then 搜索结果正确显示相关商品