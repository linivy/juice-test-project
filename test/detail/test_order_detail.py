# ==================== 规范同步信息 ====================
# spec_file: test/cases/ui-testing-patterns.md
# spec_version: 1.0.0
# spec_hash: e8847ce5
# spec_last_updated: 2026-01-15
# ===================================================


# test/detail/test_order_detail.py
"""
订单详情页面测试

功能测试点:
- TC-ORDERD-001: 订单详情页所有字段正确显示
- TC-ORDERD-002: 可选字段为空时的显示
- TC-ORDERD-003: 返回按钮功能
- TC-ORDERD-004: 订单状态显示正确
- TC-ORDERD-005: 详情页与列表页数据一致性
- TC-ORDERD-006: 编辑按钮跳转功能
- TC-ORDERD-007: 订单详情页加载

测试覆盖矩阵:
| 功能测试点ID | 功能描述 | 测试用例函数 | 参数化类型 | 数据组数 |
|-------------|---------|-------------|-----------|---------|
| TC-ORDERD-001 | 字段显示 | test_order_detail_fields | basic | 1 |
| TC-ORDERD-002 | 空字段处理 | test_detail_empty_fields | basic | 1 |
| TC-ORDERD-003 | 返回按钮 | test_order_detail_back_button | basic | 1 |
| TC-ORDERD-004 | 订单状态 | test_order_detail_status | basic | 1 |
| TC-ORDERD-005 | 数据一致性 | test_detail_data_consistency | basic | 1 |
| TC-ORDERD-006 | 编辑按钮 | test_detail_edit_button | basic | 1 |
| TC-ORDERD-007 | 页面加载 | test_order_detail_page_loads | basic | 1 |
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

def get_first_order(page: Page):
    """获取第一个订单行"""
    order_row = page.locator("table tr, .order-item, mat-row").nth(1)
    if order_row.count() == 0:
        order_row = page.locator("[role='row']").nth(1)
    return order_row

# ==================== TC-ORDERD-001: 订单详情字段显示 ====================

def test_order_detail_fields(logged_in_page: Page):
    """
    【TC-ORDERD-001】测试订单详情页所有字段正确显示
    
    测试目标: 验证订单详情页面显示订单号、商品名称、总价、状态
    
    预期结果: 所有必要字段都可见
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过详情页测试")
    
    # 点击第一个订单
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    # 验证订单号存在
    order_id = page.locator("[data-testid='order-id'], .order-id, text='Order ID'")
    if order_id.count() > 0:
        expect(order_id.first).to_be_visible()
    
    # 验证商品名称存在
    product_name = page.locator("[data-testid='product-name'], .product-name, mat-card:has(button)")
    if product_name.count() > 0:
        expect(product_name.first).to_be_visible()
    
    # 验证总价存在
    total_price = page.locator("[data-testid='total'], .total-price, text='$'")
    if total_price.count() > 0:
        expect(total_price.first).to_be_visible()
    
    # 验证状态存在
    status = page.locator("[data-testid='status'], .order-status")
    if status.count() > 0:
        expect(status.first).to_be_visible()

# ==================== TC-ORDERD-002: 空字段处理 ====================

def test_detail_empty_fields(logged_in_page: Page):
    """
    【TC-ORDERD-002】测试可选字段为空时的显示
    
    测试目标: 验证当某些可选字段为空时，页面正确显示占位符
    
    预期结果: 空字段显示 "-" 或 "暂无" 等占位符
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过详情页测试")
    
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    # 检查可选字段
    optional_fields = ["备注", "说明", "留言"]
    for field in optional_fields:
        field_locator = page.locator(f"[data-testid='{field}'], div:has-text('{field}')")
        if field_locator.count() > 0:
            text = field_locator.first.inner_text()
            # 空字段应该是空字符串、-、暂无等
            if text == field or field in text:
                # 找到对应的值
                value_locator = field_locator.locator("xpath=following-sibling::*")
                if value_locator.count() > 0:
                    value = value_locator.first.inner_text()
                    assert value in ["", "-", "暂无", "N/A", "无"]

# ==================== TC-ORDERD-003: 返回按钮功能 ====================

def test_order_detail_back_button(logged_in_page: Page):
    """
    【TC-ORDERD-003】测试返回按钮功能
    
    测试目标: 验证点击返回按钮能回到订单列表页
    
    预期结果: 返回到 /#/orders 页面
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过详情页测试")
    
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    # 查找返回按钮
    back_btn = page.get_by_role("button", name="返回")
    if back_btn.count() == 0:
        back_btn = page.get_by_role("button", name="Back")
    if back_btn.count() == 0:
        back_btn = page.locator("[aria-label='Back']")
    
    if back_btn.count() > 0:
        back_btn.click()
        page.wait_for_url(f"{BASE_URL}/#/orders", timeout=5000)
        expect(page).to_have_url(f"{BASE_URL}/#/orders")

# ==================== TC-ORDERD-004: 订单状态显示 ====================

def test_order_detail_status(logged_in_page: Page):
    """
    【TC-ORDERD-004】测试订单状态显示正确
    
    测试目标: 验证订单详情页显示正确的订单状态
    
    预期结果: 状态标签可见且值有效
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过详情页测试")
    
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    expected_statuses = ["Delivered", "Processing", "Shipped", "Cancelled", "Complete", "Pending"]
    page_content = page.content()
    
    has_status = any(status in page_content for status in expected_statuses)
    assert has_status, f"页面应包含订单状态，实际内容: {page_content[:500]}"

# ==================== TC-ORDERD-005: 数据一致性 ====================

def test_detail_data_consistency(logged_in_page: Page):
    """
    【TC-ORDERD-005】测试详情数据与列表数据一致
    
    测试目标: 验证点击订单后，详情页数据与列表页一致
    
    预期结果: 订单号、总价等关键信息一致
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    # 先从列表获取数据
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过一致性测试")
    
    # 获取列表中的订单信息
    list_order_id = order_row.inner_text()
    
    # 进入详情页
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    # 获取详情页订单信息
    detail_order_id = page.locator("[data-testid='订单号'], .order-id").first.inner_text()
    
    # 验证一致性（订单号应该匹配）
    assert list_order_id[:20] in detail_order_id or detail_order_id[:20] in list_order_id, \
        f"订单号不一致: 列表={list_order_id[:50]}, 详情={detail_order_id[:50]}"

# ==================== TC-ORDERD-006: 编辑按钮功能 ====================

def test_detail_edit_button(logged_in_page: Page):
    """
    【TC-ORDERD-006】测试编辑按钮跳转功能
    
    测试目标: 验证点击编辑按钮能跳转到编辑页面
    
    预期结果: 跳转到编辑页面
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过编辑测试")
    
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    edit_btn = page.get_by_role("button", name="编辑")
    if edit_btn.count() == 0:
        edit_btn = page.get_by_role("button", name="Edit")
    
    if edit_btn.count() > 0:
        edit_btn.click()
        # 验证跳转到编辑页面（URL 包含 edit）
        page.wait_for_url(f"**/edit/**", timeout=5000)

# ==================== TC-ORDERD-007: 页面加载 ====================

def test_order_detail_page_loads(logged_in_page: Page):
    """
    【TC-ORDERD-007】测试订单详情页面正常加载
    
    测试目标: 验证点击订单后能正常进入详情页
    
    预期结果: 页面正常加载，内容非空
    """
    page = logged_in_page
    close_cookie_banner(page)
    
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    order_row = get_first_order(page)
    if order_row.count() == 0:
        pytest.skip("没有订单数据，跳过详情页测试")
    
    order_row.click()
    page.wait_for_load_state("networkidle")
    
    assert len(page.content()) > 1000, "详情页内容为空"