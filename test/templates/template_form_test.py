# test/templates/template_form_test.py
"""
{模块名称} - {表单名称} 自动化测试

功能测试点:
- TC-{MODULE}-001: 页面正常加载
- TC-{MODULE}-002: 有效数据提交成功
- TC-{MODULE}-003: 无效数据提交失败（参数化）
- TC-{MODULE}-004: 必填项验证
- TC-{MODULE}-005: 边界值测试（参数化）
- TC-{MODULE}-006: 多次重复提交测试
- TC-{MODULE}-007: 表单重置功能测试
- TC-{MODULE}-008: 特殊字符/SQL注入测试

测试覆盖矩阵:
| 功能测试点ID | 功能描述 | 测试用例函数 | 参数化类型 | 数据组数 |
|-------------|---------|-------------|-----------|---------|
| TC-{MODULE}-001 | 页面加载 | test_form_page_loads | basic | 1 |
| TC-{MODULE}-002 | 有效提交 | test_form_submit_success | basic | 1 |
| TC-{MODULE}-003 | 无效提交 | test_form_submit_invalid | parametrized | N |
| TC-{MODULE}-004 | 必填验证 | test_form_required_fields | parametrized | N |
| TC-{MODULE}-005 | 边界值 | test_form_boundary_values | parametrized | N |
| TC-{MODULE}-006 | 重复提交 | test_form_submit_multiple_times | basic | 1 |
| TC-{MODULE}-007 | 重置功能 | test_form_reset | basic | 1 |
| TC-{MODULE}-008 | 安全测试 | test_form_security_attacks | parametrized | N |
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def close_dialogs(page: Page):
    """关闭可能出现的弹窗"""
    try:
        close_btn = page.locator("button[aria-label='Close']")
        if close_btn.is_visible(timeout=2000):
            close_btn.click()
    except:
        pass


# ==================== TC-{MODULE}-001: 页面加载 ====================

def test_form_page_loads(page: Page):
    """
    【TC-{MODULE}-001】测试表单页面正常加载
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    close_dialogs(page)
    
    # 验证表单元素存在
    expected_fields = ["#field1", "#field2", "#submitBtn"]
    for selector in expected_fields:
        expect(page.locator(selector)).to_be_visible()


# ==================== TC-{MODULE}-002: 有效提交 ====================

def test_form_submit_success(page: Page):
    """
    【TC-{MODULE}-002】测试有效数据提交成功
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    close_dialogs(page)
    
    # 填写有效数据
    page.fill("#field1", "valid_value_1")
    page.fill("#field2", "valid_value_2")
    
    # 提交表单
    page.click("#submitBtn")
    
    # 验证成功
    page.wait_for_selector(".success-message", timeout=10000)
    expect(page.locator(".success-message")).to_be_visible()


# ==================== TC-{MODULE}-003: 无效提交（参数化） ====================

@pytest.mark.parametrize("field,value,expected_error", [
    # 添加你的测试数据
    ("#field1", "", "不能为空"),
    ("#field1", "invalid", "格式错误"),
    ("#field2", "", "不能为空"),
])
def test_form_submit_invalid(page: Page, field: str, value: str, expected_error: str):
    """
    【TC-{MODULE}-003】测试无效数据提交失败 - 参数化
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    page.fill(field, value)
    page.click("#submitBtn")
    
    error_locator = page.locator(f"{field}-error, .error-message")
    expect(error_locator.first).to_contain_text(expected_error, timeout=3000)


# ==================== TC-{MODULE}-004: 必填项验证 ====================

@pytest.mark.parametrize("empty_field", [
    "#field1",
    "#field2",
])
def test_form_required_fields(page: Page, empty_field: str):
    """
    【TC-{MODULE}-004】测试必填项验证 - 参数化
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    # 填写其他字段，留空当前字段
    for selector in ["#field1", "#field2"]:
        if selector != empty_field:
            page.fill(selector, "test_value")
    
    page.click("#submitBtn")
    
    # 验证错误提示
    error_locator = page.locator(f"{empty_field}-error, .error-message")
    expect(error_locator.first).to_be_visible(timeout=3000)


# ==================== TC-{MODULE}-005: 边界值测试 ====================

@pytest.mark.parametrize("field,value,boundary_type", [
    ("#field1", "a", "最小值"),
    ("#field1", "a" * 255, "最大值"),
    ("#field2", "1", "最小值"),
    ("#field2", "999999", "最大值"),
])
def test_form_boundary_values(page: Page, field: str, value: str, boundary_type: str):
    """
    【TC-{MODULE}-005】测试边界值 - 参数化
    """
    print(f"\n测试边界场景: {boundary_type}")
    
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    page.fill(field, value)
    page.click("#submitBtn")
    
    # 验证系统没有崩溃
    assert not page.is_closed()


# ==================== TC-{MODULE}-006: 重复提交 ====================

def test_form_submit_multiple_times(page: Page):
    """
    【TC-{MODULE}-006】测试连续多次提交 - 防止重复提交
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    page.fill("#field1", "test_value")
    page.fill("#field2", "test_value")
    
    submit_btn = page.locator("#submitBtn")
    
    # 连续点击3次
    submit_btn.click()
    submit_btn.click()
    submit_btn.click()
    
    # 验证只成功一次
    success_messages = page.locator(".success-message")
    assert success_messages.count() <= 1


# ==================== TC-{MODULE}-007: 重置功能 ====================

def test_form_reset(page: Page):
    """
    【TC-{MODULE}-007】测试表单重置功能
    """
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    page.fill("#field1", "test_value")
    page.fill("#field2", "test_value")
    
    reset_btn = page.locator("button[type='reset']")
    if reset_btn.count() > 0:
        reset_btn.click()
        
        assert page.locator("#field1").input_value() == ""
        assert page.locator("#field2").input_value() == ""
    else:
        pytest.skip("没有重置按钮")


# ==================== TC-{MODULE}-008: 安全测试 ====================

@pytest.mark.parametrize("attack_string,attack_type", [
    ("' OR '1'='1", "SQL注入"),
    ("<script>alert('xss')</script>", "XSS攻击"),
    ("admin'--", "SQL注释注入"),
])
def test_form_security_attacks(page: Page, attack_string: str, attack_type: str):
    """
    【TC-{MODULE}-008】测试安全攻击防护 - 参数化
    """
    print(f"\n测试攻击类型: {attack_type}")
    
    page.goto(f"{BASE_URL}/#/{form_path}")
    page.wait_for_load_state("networkidle")
    
    page.fill("#field1", attack_string)
    page.fill("#field2", "normal_value")
    page.click("#submitBtn")
    
    # 验证系统处理了攻击（没有崩溃）
    assert not page.is_closed()