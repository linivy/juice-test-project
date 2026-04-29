# 搜索功能测试点

## 功能概述
用户登录后可以通过关键词搜索商品

## 自动化覆盖情况
| 测试点 | 自动化文件 | 函数名 | 状态 |
|--------|-----------|--------|------|
| TC-SEARCH-001 | test_search.py | test_search_exact_match | ✅ 已自动化 |
| TC-SEARCH-002 | test_search.py | test_search_partial_match | ✅ 已自动化 |
| TC-SEARCH-003 | test_search.py | test_search_no_match | ✅ 已自动化 |
| TC-SEARCH-004 | test_search.py | test_search_empty_string | ✅ 已自动化 |
| TC-SEARCH-005 | test_product_list.py | test_product_list_search | ✅ 已自动化 |

## 未自动化的测试点
- [ ] TC-SEARCH-006: 搜索后点击搜索结果跳转详情
- [ ] TC-SEARCH-007: 搜索历史记录
- [ ] TC-SEARCH-008: 热门搜索词推荐
- [ ] TC-SEARCH-009: 搜索建议下拉框
- [ ] TC-SEARCH-010: 中英文混合搜索

## BDD 格式
### TC-SEARCH-001
Given 用户已登录
When 用户输入 "Apple Juice" 并搜索
Then 搜索结果中显示 "Apple Juice"

### TC-SEARCH-002
Given 用户已登录
When 用户输入 "Apple" 并搜索
Then 显示所有包含 "Apple" 的商品

### TC-SEARCH-003
Given 用户已登录
When 用户输入 "NonExistent" 并搜索
Then 显示 "No results found"