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
    
    # Assert
    expected_columns = ["商品名称", "价格", "库存"]
    for col in expected_columns:
        col_locator = page.locator(f"th:has-text('{col}')")
        assert col_locator.count() > 0, f"列 '{col}' 不存在"


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
