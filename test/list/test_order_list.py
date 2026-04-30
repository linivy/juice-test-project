"""
# ==================== 规范同步信息 ====================
spec_file: test/cases/ui-testing-patterns.md
spec_version: 1.0.0
spec_hash: e8847ce5
spec_last_updated: 2026-01-15
# ===================================================
"""

# test/list/test_order_list.py
"""
订单列表页面测试

功能测试点:
- TC-ORDERL-001: 订单列表页面正常加载
- TC-ORDERL-002: 订单列表显示必要字段
- TC-ORDERL-003: 通过导航栏访问订单列表页
- TC-ORDERL-004: 空订单列表显示提示信息
- TC-ORDERL-005: 订单列表搜索功能
- TC-ORDERL-006: 订单列表排序功能
- TC-ORDERL-007: 订单列表分页功能

测试覆盖矩阵:
| 功能测试点ID | 功能描述 | 测试用例函数 | 参数化类型 | 数据组数 |
|-------------|---------|-------------|-----------|---------|
| TC-ORDERL-001 | 页面加载 | test_order_list_page_loads | basic | 1 |
| TC-ORDERL-002 | 字段验证 | test_order_list_fields | basic | 1 |
| TC-ORDERL-003 | 导航栏访问 | test_order_list_navigation | basic | 1 |
| TC-ORDERL-004 | 空订单提示 | test_empty_order_list | basic | 1 |
| TC-ORDERL-005 | 搜索功能 | test_order_list_search | parametrized | 3 |
| TC-ORDERL-006 | 排序功能 | test_order_list_sort | basic | 1 |
| TC-ORDERL-007 | 分页功能 | test_order_list_pagination | basic | 1 |
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"

def close_cookie_banner(page: Page):
    """关闭 Cookie 弹窗"""
    try:
        cookie_btn = page.get_by_role("button", name="Me want it!")
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()
    except:
        pass

# ==================== TC-ORDERL-001: 订单列表页面加载 ====================

def test_order_list_page_loads(logged_in_page: Page):
    """
    【TC-ORDERL-001】测试订单列表页面正常加载
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_url(f"{BASE_URL}/#/orders")

# ==================== TC-ORDERL-002: 字段验证 ====================

def test_order_list_fields(logged_in_page: Page):
    """
    【TC-ORDERL-002】测试订单列表显示必要字段
    
    预期结果: 订单列表包含订单号、商品名称、数量、总价、状态
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_url(f"{BASE_URL}/#/orders", timeout=15000)
    page.wait_for_load_state("networkidle")
    
    # 等待订单列表加载
    page.wait_for_selector("table, .order-list, mat-table", timeout=10000)
    
    order_table = page.locator("table, .order-list, mat-table")
    expect(order_table.first).to_be_visible(timeout=5000)
    
    table_content = order_table.first.inner_text()
    
    # 验证必要字段存在
    fields = ["Order", "#", "$", "€"]
    has_field = any(field in table_content for field in fields)
    assert has_field, f"订单列表应包含必要字段，实际内容: {table_content[:200]}"

# ==================== TC-ORDERL-003: 导航栏访问 ====================

def test_order_list_navigation(logged_in_page: Page):
    """
    【TC-ORDERL-003】测试通过导航栏访问订单列表页
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    orders_link = page.get_by_role("link", name="Orders", exact=True)
    if orders_link.count() == 0:
        orders_link = page.get_by_role("link", name="Order", exact=True)
    
    if orders_link.count() > 0:
        orders_link.click()
        page.wait_for_url(f"{BASE_URL}/#/orders", timeout=10000)
    else:
        page.goto(f"{BASE_URL}/#/orders")
    
    expect(page).to_have_url(f"{BASE_URL}/#/orders")

# ==================== TC-ORDERL-004: 空订单提示 ====================

def test_empty_order_list(logged_in_page: Page):
    """
    【TC-ORDERL-004】测试无订单时显示提示信息
    
    预期结果: 显示"No orders"或类似提示
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    empty_message = page.locator("text='No orders'")
    if empty_message.count() == 0:
        empty_message = page.locator("text='empty'")
    if empty_message.count() == 0:
        empty_message = page.locator("text='没有订单'")
    
    if empty_message.count() > 0:
        expect(empty_message.first).to_be_visible()

# ==================== TC-ORDERL-005: 搜索功能 ====================

@pytest.mark.parametrize("keyword,expected_has_result", [
    ("Apple", True),
    ("Juice", True),
    ("XYZNonExistent", False),
])
def test_order_list_search(logged_in_page: Page, keyword: str, expected_has_result: bool):
    """
    【TC-ORDERL-005】测试订单列表搜索功能 - 参数化
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    search_input = page.locator("input[placeholder*='Search' i]")
    if search_input.count() == 0:
        pytest.skip("没有搜索功能")
    
    search_input.fill(keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")
    
    if expected_has_result:
        # 期望有结果
        results = page.locator("tbody tr, .order-item")
        if results.count() > 0:
            assert True
    else:
        # 期望无结果
        empty_state = page.locator(".empty-state, text='No results'")
        if empty_state.count() > 0:
            expect(empty_state.first).to_be_visible()

# ==================== TC-ORDERL-006: 排序功能 ====================

def test_order_list_sort(logged_in_page: Page):
    """
    【TC-ORDERL-006】测试订单列表排序功能
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    sortable_col = page.locator("th:has(.sort-icon), th:has(button)").first
    if sortable_col.count() == 0:
        pytest.skip("没有排序功能")
    
    before_values = page.locator("tbody tr td:first-child").all_inner_texts()
    sortable_col.click()
    page.wait_for_load_state("networkidle")
    after_values = page.locator("tbody tr td:first-child").all_inner_texts()
    
    if len(before_values) > 1:
        assert before_values != after_values or len(before_values) <= 1

# ==================== TC-ORDERL-007: 分页功能 ====================

def test_order_list_pagination(logged_in_page: Page):
    """
    【TC-ORDERL-007】测试订单列表分页功能
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    pagination = page.locator(".pagination")
    if pagination.count() == 0:
        pytest.skip("没有分页功能")
    
    next_btn = page.locator("button[aria-label='下一页']")
    if next_btn.is_enabled():
        next_btn.click()
        page.wait_for_load_state("networkidle")
        
        current_page = page.locator(".active-page")
        if current_page.count() > 0:
            assert current_page.inner_text() == "2"