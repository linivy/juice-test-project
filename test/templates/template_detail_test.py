# test/templates/template_detail_test.py
"""
{模块名称} - 详情页自动化测试

功能测试点:
- TC-{MODULE}D-001: 详情页所有字段正确显示
- TC-{MODULE}D-002: 可选字段为空时的显示
- TC-{MODULE}D-003: 返回按钮功能
- TC-{MODULE}D-004: 状态显示正确
- TC-{MODULE}D-005: 详情页与列表页数据一致性
- TC-{MODULE}D-006: 编辑按钮跳转功能
- TC-{MODULE}D-007: 详情页加载
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def get_first_item(page: Page):
    """获取第一个列表项"""
    item = page.locator("tbody tr, .item-list > div, mat-row").first
    return item


# ==================== TC-{MODULE}D-001: 字段显示 ====================

def test_detail_fields_display(page: Page):
    """
    【TC-{MODULE}D-001】测试详情页所有字段正确显示
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    # 验证各字段存在
    expected_field_selectors = ["#field1", "#field2", "#field3"]
    for selector in expected_field_selectors:
        expect(page.locator(selector)).to_be_visible()


# ==================== TC-{MODULE}D-002: 空字段处理 ====================

def test_detail_empty_fields(page: Page):
    """
    【TC-{MODULE}D-002】测试可选字段为空时的显示
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    optional_fields = ["备注", "说明", "留言"]
    for field in optional_fields:
        field_locator = page.locator(f"text='{field}'")
        if field_locator.count() > 0:
            value = field_locator.locator("xpath=following-sibling::*").first.inner_text()
            assert value in ["", "-", "暂无", "N/A"]


# ==================== TC-{MODULE}D-003: 返回按钮 ====================

def test_detail_back_button(page: Page):
    """
    【TC-{MODULE}D-003】测试返回按钮功能
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    back_btn = page.get_by_role("button", name="返回")
    if back_btn.count() == 0:
        back_btn = page.get_by_role("button", name="Back")
    
    if back_btn.count() > 0:
        back_btn.click()
        page.wait_for_url(f"{BASE_URL}/#/{list_path}", timeout=5000)


# ==================== TC-{MODULE}D-004: 状态显示 ====================

def test_detail_status(page: Page):
    """
    【TC-{MODULE}D-004】测试状态显示正确
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    expected_statuses = ["Active", "Inactive", "Pending", "Complete"]
    page_content = page.content()
    
    has_status = any(status in page_content for status in expected_statuses)
    assert has_status, "页面应包含状态信息"


# ==================== TC-{MODULE}D-005: 数据一致性 ====================

def test_detail_data_consistency(page: Page):
    """
    【TC-{MODULE}D-005】测试详情数据与列表数据一致
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    list_title = first_item.inner_text()[:50]
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    detail_title = page.locator("h1, .title").first.inner_text()
    
    assert list_title in detail_title or detail_title in list_title


# ==================== TC-{MODULE}D-006: 编辑按钮 ====================

def test_detail_edit_button(page: Page):
    """
    【TC-{MODULE}D-006】测试编辑按钮跳转功能
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    edit_btn = page.get_by_role("button", name="编辑")
    if edit_btn.count() == 0:
        edit_btn = page.get_by_role("button", name="Edit")
    
    if edit_btn.count() > 0:
        edit_btn.click()
        page.wait_for_url(f"**/edit/**", timeout=5000)


# ==================== TC-{MODULE}D-007: 页面加载 ====================

def test_detail_page_loads(page: Page):
    """
    【TC-{MODULE}D-007】测试详情页面正常加载
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_item = get_first_item(page)
    if first_item.count() == 0:
        pytest.skip("没有数据")
    
    first_item.click()
    page.wait_for_load_state("networkidle")
    
    assert len(page.content()) > 1000, "详情页内容为空"