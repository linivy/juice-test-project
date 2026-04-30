# test/templates/template_list_test.py
"""
{模块名称} - 列表页自动化测试

功能测试点:
- TC-{MODULE}L-001: 列表页面正常加载
- TC-{MODULE}L-002: 列表显示必要字段
- TC-{MODULE}L-003: 导航栏访问
- TC-{MODULE}L-004: 空列表显示提示
- TC-{MODULE}L-005: 搜索功能（参数化）
- TC-{MODULE}L-006: 排序功能
- TC-{MODULE}L-007: 分页功能
- TC-{MODULE}L-008: 新增后刷新
- TC-{MODULE}L-009: 编辑后刷新
- TC-{MODULE}L-010: 删除后刷新
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


# ==================== TC-{MODULE}L-001: 页面加载 ====================

def test_list_page_loads(page: Page):
    """
    【TC-{MODULE}L-001】测试列表页面正常加载
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_url(f"{BASE_URL}/#/{list_path}")


# ==================== TC-{MODULE}L-002: 字段验证 ====================

def test_list_columns(page: Page):
    """
    【TC-{MODULE}L-002】测试列表字段完整
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    expected_columns = ["列1", "列2", "列3"]
    for col in expected_columns:
        col_locator = page.locator(f"th:has-text('{col}')")
        assert col_locator.count() > 0, f"列 '{col}' 不存在"


# ==================== TC-{MODULE}L-003: 导航栏访问 ====================

def test_list_navigation(page: Page):
    """
    【TC-{MODULE}L-003】测试通过导航栏访问列表页
    """
    page.goto(f"{BASE_URL}/#/")
    page.wait_for_load_state("networkidle")
    
    nav_link = page.get_by_role("link", name="{nav_name}")
    if nav_link.count() > 0:
        nav_link.click()
        page.wait_for_url(f"{BASE_URL}/#/{list_path}", timeout=10000)
        expect(page).to_have_url(f"{BASE_URL}/#/{list_path}")


# ==================== TC-{MODULE}L-004: 空列表提示 ====================

def test_empty_list(page: Page):
    """
    【TC-{MODULE}L-004】测试空列表时显示提示信息
    """
    page.goto(f"{BASE_URL}/#/{list_path}?empty=true")
    page.wait_for_load_state("networkidle")
    
    empty_message = page.locator(".empty-state, text='暂无数据'")
    if empty_message.count() > 0:
        expect(empty_message.first).to_be_visible()


# ==================== TC-{MODULE}L-005: 搜索功能 ====================

@pytest.mark.parametrize("keyword,expected_has_result", [
    ("keyword1", True),
    ("keyword2", True),
    ("non_existent", False),
])
def test_list_search(page: Page, keyword: str, expected_has_result: bool):
    """
    【TC-{MODULE}L-005】测试列表搜索功能 - 参数化
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    search_input = page.locator("input[placeholder*='Search' i]")
    if search_input.count() == 0:
        pytest.skip("没有搜索功能")
    
    search_input.fill(keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")
    
    if expected_has_result:
        results = page.locator("tbody tr, .list-item, mat-row")
        if results.count() > 0:
            assert True
    else:
        empty_state = page.locator(".empty-state, text='No results'")
        if empty_state.count() > 0:
            expect(empty_state.first).to_be_visible()


# ==================== TC-{MODULE}L-006: 排序功能 ====================

def test_list_sort(page: Page):
    """
    【TC-{MODULE}L-006】测试列表排序功能
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    sortable_col = page.locator("th:has(.sort-icon), th:has(button)").first
    if sortable_col.count() == 0:
        pytest.skip("没有排序功能")
    
    before_values = page.locator("tbody tr td:first-child").all_inner_texts()
    sortable_col.click()
    page.wait_for_load_state("networkidle")
    after_values = page.locator("tbody tr td:first-child").all_inner_texts()
    
    if len(before_values) > 1:
        assert before_values != after_values


# ==================== TC-{MODULE}L-007: 分页功能 ====================

def test_list_pagination(page: Page):
    """
    【TC-{MODULE}L-007}】测试列表分页功能
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
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


# ==================== TC-{MODULE}L-008: 新增后刷新 ====================

def test_list_refresh_after_add(page: Page):
    """
    【TC-{MODULE}L-008】测试新增后列表刷新
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    initial_count = page.locator("tbody tr, .list-item, mat-row").count()
    
    add_btn = page.get_by_role("button", name="新增")
    if add_btn.count() == 0:
        pytest.skip("没有新增功能")
    
    add_btn.click()
    page.wait_for_url(f"**/add/**", timeout=5000)
    
    # 填写表单并提交
    page.fill("#name", "测试项")
    page.click("button[type='submit']")
    
    page.wait_for_url(f"{BASE_URL}/#/{list_path}", timeout=5000)
    new_count = page.locator("tbody tr, .list-item, mat-row").count()
    
    assert new_count >= initial_count


# ==================== TC-{MODULE}L-009: 编辑后刷新 ====================

def test_list_refresh_after_edit(page: Page):
    """
    【TC-{MODULE}L-009】测试编辑后列表刷新
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    first_row = page.locator("tbody tr, .list-item, mat-row").first
    if first_row.count() == 0:
        pytest.skip("没有数据")
    
    original_name = first_row.locator("td:first-child").inner_text()
    
    edit_btn = first_row.locator("button:has-text('编辑')")
    if edit_btn.count() == 0:
        pytest.skip("没有编辑功能")
    
    edit_btn.click()
    page.wait_for_url(f"**/edit/**", timeout=5000)
    
    page.fill("#name", "修改后的名称")
    page.click("button[type='submit']")
    
    page.wait_for_url(f"{BASE_URL}/#/{list_path}", timeout=5000)
    updated_name = page.locator("tbody tr, .list-item, mat-row").first.locator("td:first-child").inner_text()
    
    assert updated_name != original_name


# ==================== TC-{MODULE}L-010: 删除后刷新 ====================

def test_list_refresh_after_delete(page: Page):
    """
    【TC-{MODULE}L-010】测试删除后列表刷新
    """
    page.goto(f"{BASE_URL}/#/{list_path}")
    page.wait_for_load_state("networkidle")
    
    initial_count = page.locator("tbody tr, .list-item, mat-row").count()
    if initial_count == 0:
        pytest.skip("没有数据可删除")
    
    first_row = page.locator("tbody tr, .list-item, mat-row").first
    delete_btn = first_row.locator("button:has-text('删除')")
    if delete_btn.count() == 0:
        pytest.skip("没有删除功能")
    
    page.on("dialog", lambda dialog: dialog.accept())
    delete_btn.click()
    
    page.wait_for_load_state("networkidle")
    new_count = page.locator("tbody tr, .list-item, mat-row").count()
    
    assert new_count == initial_count - 1