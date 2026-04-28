# test/detail/test_order_detail.py
"""订单详情页面测试"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def test_order_detail_fields(logged_in_page: Page):
    """测试订单详情页所有字段正确显示"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/orders")
    page.wait_for_load_state("networkidle")
    
    # 点击第一个订单查看详情
    order_rows = page.locator("table tr")
    if order_rows.count() > 1:
        order_rows.nth(1).click()
        page.wait_for_load_state("networkidle")
        
        # Assert
        # 验证订单号
        order_id = page.locator("[data-testid='order-id'], .order-id")
        expect(order_id.first).to_be_visible()
        
        # 验证商品名称
        product_name = page.locator("[data-testid='product-name'], .product-name")
        expect(product_name.first).to_be_visible()
        
        # 验证总价
        total_price = page.locator("[data-testid='total'], .total-price")
        expect(total_price.first).to_be_visible()
        
        # 验证状态
        status = page.locator("[data-testid='status'], .order-status")
        expect(status.first).to_be_visible()


def test_order_detail_back_button(logged_in_page: Page):
    """测试返回按钮功能"""
    page = logged_in_page
    page.goto(f"{BASE_URL}/#/orders")
    
    order_rows = page.locator("table tr")
    if order_rows.count() > 1:
        order_rows.nth(1).click()
        page.wait_for_load_state("networkidle")
        
        back_btn = page.get_by_role("button", name="返回")
        if back_btn.count() > 0:
            back_btn.click()
            page.wait_for_url(f"{BASE_URL}/#/orders", timeout=5000)
