---
name: ui-testing-patterns
description: UI 测试模式规范 - 表单页/详情页/列表页的测试规则
trigger: manual
type: pattern
---

# UI 测试模式规范

## 1. 表单页面测试

### 1.1 主场景测试

```python
def test_form_submit_success(page: Page, base_url: str):
    """测试表单正常提交 - 有效输入后提交成功"""
    # Arrange
    page.goto(f"{base_url}/#/form-page")
    page.wait_for_load_state("networkidle")
    
    # Act
    page.fill("#username", "testuser")
    page.fill("#email", "test@example.com")
    page.fill("#password", "Test123456")
    page.click("button[type='submit']")
    
    # Assert
    page.wait_for_selector(".success-message", timeout=5000)
    expect(page.locator(".success-message")).to_be_visible()
```

### 1.2 字段校验测试

```python
@pytest.mark.parametrize("field,value,expected_error", [
    ("username", "", "用户名不能为空"),
    ("email", "invalid", "邮箱格式错误"),
    ("email", "a@b", "邮箱格式错误"),
    ("password", "123", "密码长度至少6位"),
    ("password", "abcdef", "密码需要包含数字"),
    ("phone", "12345", "手机号格式不正确"),
    ("age", "-1", "年龄必须大于0"),
    ("age", "200", "年龄超出范围"),
])
def test_form_field_validation(page: Page, base_url: str, field, value, expected_error):
    """测试表单字段校验 - 各字段边界和格式校验"""
    page.goto(f"{base_url}/#/form-page")
    page.fill(f"#{field}", value)
    page.click("button[type='submit']")
    
    error_locator = page.locator(f"#{field}-error, .error-message")
    expect(error_locator.first).to_contain_text(expected_error, timeout=3000)
```

### 1.3 边界值测试

```python
def test_form_boundary_values(page: Page, base_url: str):
    """测试边界值：最小值、最大值、边界外"""
    page.goto(f"{base_url}/#/form-page")
    
    # 最小值边界
    page.fill("#quantity", "1")
    page.fill("#price", "0.01")
    
    # 最大值边界
    page.fill("#quantity", "999")
    page.fill("#price", "99999.99")
    
    # 超出范围
    page.fill("#quantity", "1000")
    page.fill("#price", "100000")
    page.click("button[type='submit']")
    
    expect(page.locator(".error-message")).to_be_visible()
```

### 1.4 非常规操作测试

```python
def test_form_submit_multiple_times(page: Page, base_url: str):
    """测试连续多次提交 - 防止重复提交"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    
    # 连续点击提交按钮
    submit_btn = page.locator("button[type='submit']")
    submit_btn.click()
    submit_btn.click()
    submit_btn.click()
    
    # 验证不会重复提交（页面不会出现多个成功提示）
    success_messages = page.locator(".success-message")
    assert success_messages.count() <= 1


def test_form_submit_disabled_button(page: Page, base_url: str):
    """测试禁用状态下无法提交"""
    page.goto(f"{base_url}/#/form-page")
    
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_be_disabled()  # 表单为空时按钮应禁用
    
    page.fill("#username", "testuser")
    expect(submit_btn).to_be_enabled()  # 填写必填项后按钮应启用


def test_form_reset(page: Page, base_url: str):
    """测试表单重置功能"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    page.fill("#email", "test@example.com")
    
    reset_btn = page.locator("button[type='reset']")
    if reset_btn.count() > 0:
        reset_btn.click()
        
        assert page.locator("#username").input_value() == ""
        assert page.locator("#email").input_value() == ""


def test_form_navigation_away(page: Page, base_url: str):
    """测试填写中途离开页面的提示"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    
    # 尝试导航离开
    with page.expect_dialog() as dialog_info:
        page.goto(f"{base_url}/#/other-page")
    
    dialog = dialog_info.value
    assert "离开" in dialog.message or "确认" in dialog.message or "unsaved" in dialog.message.lower()
    dialog.dismiss()  # 取消离开

def test_form_submit_disabled_button(page: Page, base_url: str):
    """测试禁用状态下无法提交"""
    page.goto(f"{base_url}/#/form-page")
    
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_be_disabled()  # 表单为空时按钮应禁用
    
    page.fill("#username", "testuser")
    expect(submit_btn).to_be_enabled()  # 填写必填项后按钮应启用

def test_form_reset(page: Page, base_url: str):
    """测试表单重置功能"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    page.fill("#email", "test@example.com")
    
    reset_btn = page.locator("button[type='reset']")
    if reset_btn.count() > 0:
        reset_btn.click()
        
        assert page.locator("#username").input_value() == ""
        assert page.locator("#email").input_value() == ""

def test_form_navigation_away(page: Page, base_url: str):
    """测试填写中途离开页面的提示"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    
    # 尝试导航离开
    with page.expect_dialog() as dialog_info:
        page.goto(f"{base_url}/#/other-page")
    
    dialog = dialog_info.value
    assert "离开" in dialog.message or "确认" in dialog.message
    dialog.dismiss()  # 取消离开

def test_form_timeout(page: Page, base_url: str):
    """测试会话超时后重新登录"""
    page.goto(f"{base_url}/#/form-page")
    page.fill("#username", "testuser")
    
    # 模拟会话超时（通过重新登录）
    page.goto(f"{base_url}/#/login")
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    # 返回表单页
    page.goto(f"{base_url}/#/form-page")
    # 表单应该已清空或提示重新填写
```

## 2. 详情页面测试

### 2.1 字段显示测试

```python
def test_detail_fields_display(page: Page, base_url: str):
    """测试详情页所有字段正确显示"""
    page.goto(f"{base_url}/#/detail/1")
    page.wait_for_load_state("networkidle")
    
    expected_fields = {
        "订单号": "ORD-001",
        "商品名称": "Apple Juice",
        "数量": "2",
        "总价": "$3.98",
        "状态": "已发货",
        "创建时间": "2024-01-15 10:30",
    }
    
    for field_name, expected_value in expected_fields.items():
        field_locator = page.locator(
            f"[data-testid='{field_name}'], "
            f"div:has-text('{field_name}') + div"
        )
        expect(field_locator.first).to_be_visible()
        actual_value = field_locator.first.inner_text()
        assert expected_value in actual_value

def test_detail_empty_fields(page: Page, base_url: str):
    """测试可选字段为空时的显示"""
    page.goto(f"{base_url}/#/detail/empty-item")
    
    optional_fields = ["备注", "描述", "说明"]
    for field in optional_fields:
        field_locator = page.locator(f"[data-testid='{field}']")
        if field_locator.count() > 0:
            text = field_locator.first.inner_text()
            assert text in ["", "-", "暂无", "N/A"]
```

### 2.2 操作按钮测试

```python
def test_detail_edit_button(page: Page, base_url: str):
    """测试编辑按钮跳转"""
    page.goto(f"{base_url}/#/detail/1")
    
    edit_btn = page.get_by_role("button", name="编辑")
    expect(edit_btn).to_be_visible()
    edit_btn.click()
    
    page.wait_for_url(f"{base_url}/#/edit/1", timeout=5000)
    expect(page).to_have_url(f"{base_url}/#/edit/1")


def test_detail_data_consistency(page: Page, base_url: str):
    """测试详情数据与列表数据一致"""
    # 先从列表获取数据
    page.goto(f"{base_url}/#/list")
    first_row = page.locator("tbody tr").first
    list_order_id = first_row.locator("td:nth-child(1)").inner_text()
    list_total = first_row.locator("td:nth-child(4)").inner_text()
    
    # 进入详情页
    first_row.click()
    page.wait_for_load_state("networkidle")
    
    # 验证数据一致
    detail_order_id = page.locator("[data-testid='订单号'], .order-id").inner_text()
    detail_total = page.locator("[data-testid='总价'], .total-price").inner_text()
    
    assert list_order_id == detail_order_id, f"订单号不一致: 列表={list_order_id}, 详情={detail_order_id}"
    assert list_total == detail_total, f"总价不一致: 列表={list_total}, 详情={detail_total}"

def test_detail_delete_button(page: Page, base_url: str):
    """测试删除按钮功能"""
    page.goto(f"{base_url}/#/detail/1")
    
    delete_btn = page.get_by_role("button", name="删除")
    expect(delete_btn).to_be_visible()
    
    page.on("dialog", lambda dialog: dialog.accept())
    delete_btn.click()
    
    page.wait_for_url(f"{base_url}/#/list", timeout=5000)
```

### 2.3 数据持久化验证

```python
def test_detail_data_consistency(page: Page, base_url: str):
    """测试详情数据与列表数据一致"""
    # 先从列表获取数据
    page.goto(f"{base_url}/#/list")
    first_row = page.locator("tbody tr").first
    list_order_id = first_row.locator("td:nth-child(1)").inner_text()
    list_total = first_row.locator("td:nth-child(4)").inner_text()
    
    # 进入详情页
    first_row.click()
    page.wait_for_load_state("networkidle")
    
    # 验证数据一致
    detail_order_id = page.locator("[data-testid='订单号']").inner_text()
    detail_total = page.locator("[data-testid='总价']").inner_text()
    
    assert list_order_id == detail_order_id
    assert list_total == detail_total
```

## 3. 列表页面测试

### 3.1 字段验证测试

```python
def test_list_columns(page: Page, base_url: str):
    """测试列表字段完整"""
    page.goto(f"{base_url}/#/list")
    page.wait_for_load_state("networkidle")
    
    expected_columns = ["订单号", "商品名称", "数量", "总价", "状态"]
    for col in expected_columns:
        col_locator = page.locator(f"th:has-text('{col}')")
        assert col_locator.count() > 0, f"列 '{col}' 不存在"
    
    # 验证每行数据完整
    rows = page.locator("tbody tr")
    if rows.count() > 0:
        first_row = rows.first
        for i, col in enumerate(expected_columns):
            cell = first_row.locator(f"td:nth-child({i+1})")
            expect(cell).to_be_visible()
```

### 3.2 数据范围测试

```python
def test_list_data_range(page: Page, base_url: str):
    """测试列表数据范围显示正确"""
    page.goto(f"{base_url}/#/list")
    
    # 获取总数显示
    total_count_locator = page.locator(".total-count")
    if total_count_locator.count() > 0:
        import re
        total_text = total_count_locator.first.inner_text()
        numbers = re.findall(r'\d+', total_text)
        if numbers:
            total = int(numbers[0])
            rows = page.locator("tbody tr").count()
            assert rows <= total
```

### 3.3 搜索功能测试

```python
@pytest.mark.parametrize("keyword,expected_count", [
    ("Apple", 2),      # 存在的关键词
    ("Orange", 1),     # 存在的关键词
    ("XYZ123", 0),     # 不存在的关键词
])
def test_list_search(page: Page, base_url: str, keyword, expected_count):
    """测试按不同字段搜索"""
    page.goto(f"{base_url}/#/list")
    
    search_input = page.get_by_role("searchbox")
    if search_input.count() == 0:
        pytest.skip("没有搜索功能")
    
    search_input.fill(keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")
    
    results = page.locator("tbody tr")
    if expected_count > 0:
        assert results.count() >= expected_count
        first_result_text = results.first.inner_text()
        assert keyword.lower() in first_result_text.lower()
    else:
        assert results.count() == 0 or page.locator(".empty-state").is_visible()
```

### 3.4 排序功能测试

```python
def test_list_sort(page: Page, base_url: str):
    """测试列表排序"""
    page.goto(f"{base_url}/#/list")
    
    sortable_col = page.locator("th:has(.sort-icon)").first
    if sortable_col.count() == 0:
        pytest.skip("没有排序功能")
    
    before_values = page.locator("tbody tr td:nth-child(1)").all_inner_texts()
    sortable_col.click()
    page.wait_for_load_state("networkidle")
    after_values = page.locator("tbody tr td:nth-child(1)").all_inner_texts()
    
    assert before_values != after_values or len(before_values) <= 1
    
    # 再次点击验证倒序
    sortable_col.click()
    page.wait_for_load_state("networkidle")
    reverse_values = page.locator("tbody tr td:nth-child(1)").all_inner_texts()
    assert reverse_values == before_values  # 恢复原序
```

### 3.5 增删改后刷新测试

```python
def test_list_refresh_after_add(page: Page, base_url: str):
    """测试新增后列表刷新"""
    page.goto(f"{base_url}/#/list")
    initial_count = page.locator("tbody tr").count()
    
    add_btn = page.get_by_role("button", name="新增")
    if add_btn.count() == 0:
        pytest.skip("没有新增功能")
    
    add_btn.click()
    page.wait_for_url(f"{base_url}/#/add", timeout=5000)
    
    page.fill("#name", "测试商品")
    page.fill("#price", "100")
    page.click("button[type='submit']")
    
    page.wait_for_url(f"{base_url}/#/list", timeout=5000)
    new_count = page.locator("tbody tr").count()
    assert new_count == initial_count + 1

def test_list_refresh_after_update(page: Page, base_url: str):
    """测试修改后列表刷新"""
    page.goto(f"{base_url}/#/list")
    first_row = page.locator("tbody tr").first
    original_name = first_row.locator("td:nth-child(2)").inner_text()
    
    edit_btn = first_row.locator("button:has-text('编辑')")
    if edit_btn.count() == 0:
        pytest.skip("没有编辑功能")
    
    edit_btn.click()
    page.wait_for_url(f"{base_url}/#/edit/", timeout=5000)
    
    page.fill("#name", "修改后的名称")
    page.click("button[type='submit']")
    
    page.wait_for_url(f"{base_url}/#/list", timeout=5000)
    updated_name = page.locator("tbody tr").first.locator("td:nth-child(2)").inner_text()
    assert updated_name != original_name

def test_list_refresh_after_delete(page: Page, base_url: str):
    """测试删除后列表刷新"""
    page.goto(f"{base_url}/#/list")
    initial_count = page.locator("tbody tr").count()
    if initial_count == 0:
        pytest.skip("没有数据可删除")
    
    first_row = page.locator("tbody tr").first
    delete_btn = first_row.locator("button:has-text('删除')")
    if delete_btn.count() == 0:
        pytest.skip("没有删除按钮")
    
    page.on("dialog", lambda dialog: dialog.accept())
    delete_btn.click()
    
    page.wait_for_load_state("networkidle")
    new_count = page.locator("tbody tr").count()
    assert new_count == initial_count - 1
```

### 3.6 导出功能测试

```python
def test_list_export(page: Page, base_url: str):
    """测试列表导出功能"""
    page.goto(f"{base_url}/#/list")
    
    export_btn = page.get_by_role("button", name="导出")
    if export_btn.count() == 0:
        pytest.skip("没有导出功能")
    
    with page.expect_download() as download_info:
        export_btn.click()
    
    download = download_info.value
    assert download.suggested_filename.endswith(('.csv', '.xlsx', '.pdf'))
    
    # 验证文件内容
    import tempfile
    import os
    temp_dir = tempfile.gettempdir()
    save_path = os.path.join(temp_dir, download.suggested_filename)
    download.save_as(save_path)
    assert os.path.getsize(save_path) > 0
    os.remove(save_path)
```

### 3.7 分页功能测试

```python
def test_list_pagination(page: Page, base_url: str):
    """测试分页功能"""
    page.goto(f"{base_url}/#/list")
    
    pagination = page.locator(".pagination")
    if pagination.count() == 0:
        pytest.skip("没有分页功能")
    
    first_page_rows = page.locator("tbody tr").count()
    
    next_btn = page.locator("button[aria-label='下一页']")
    if next_btn.is_enabled():
        next_btn.click()
        page.wait_for_load_state("networkidle")
        
        current_page = page.locator(".active-page")
        if current_page.count() > 0:
            assert current_page.inner_text() == "2"


def test_list_pagination_navigation(page: Page, base_url: str):
    """测试分页导航：首页、末页、跳页"""
    page.goto(f"{base_url}/#/list")
    
    pagination = page.locator(".pagination")
    if pagination.count() == 0:
        pytest.skip("没有分页功能")
    
    # 测试跳转到末页
    last_btn = page.locator("button[aria-label='末页'], .last-page")
    if last_btn.count() > 0 and last_btn.is_enabled():
        last_btn.click()
        page.wait_for_load_state("networkidle")
        
        # 验证末页的下一页按钮应该禁用
        next_btn = page.locator("button[aria-label='下一页']")
        expect(next_btn).to_be_disabled()
    
    # 测试跳转到首页
    first_btn = page.locator("button[aria-label='首页'], .first-page")
    if first_btn.count() > 0:
        first_btn.click()
        page.wait_for_load_state("networkidle")
        
        # 验证首页的上一页按钮应该禁用
        prev_btn = page.locator("button[aria-label='上一页']")
        expect(prev_btn).to_be_disabled()


def test_list_pagination_page_size(page: Page, base_url: str):
    """测试分页每页条数选择"""
    page.goto(f"{base_url}/#/list")
    
    page_size_select = page.locator("select[name='pageSize'], .page-size-select")
    if page_size_select.count() == 0:
        pytest.skip("没有每页条数选择功能")
    
    original_count = page.locator("tbody tr").count()
    
    # 选择更大的每页条数
    page_size_select.select_option("20")
    page.wait_for_load_state("networkidle")
    
    new_count = page.locator("tbody tr").count()
    assert new_count >= original_count  # 显示更多数据
```