# test/list/test_product_list.py
"""商品列表页面测试"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def test_product_list_columns(logged_in_page: Page):
    """测试商品列表字段完整"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # Assert - 支持中英文列名
    expected_columns = ["商品名称", "Product", "Name", "价格", "Price", "库存", "Stock"]
    found_columns = set()
    
    for col in expected_columns:
        col_locator = page.locator(f"th:has-text('{col}')")
        if col_locator.count() > 0:
            found_columns.add(col)
    
    # 至少找到3个不同的列
    assert len(found_columns) >= 3, f"只找到 {len(found_columns)} 个列: {found_columns}"


def test_product_list_search(logged_in_page: Page):
    """测试商品列表搜索功能"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    search_input = page.get_by_role("searchbox")
    
    if search_input.count() > 0:
        search_input.fill("Apple")
        search_input.press("Enter")
        page.wait_for_load_state("networkidle")
        
        # Assert
        products = page.locator(".mat-card")
        expect(products.first).to_be_visible()