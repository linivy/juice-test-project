# test/list/test_product_list.py
"""商品列表页面测试 - 卡片形式展示"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def test_product_list_display(logged_in_page: Page):
    """测试商品列表页面显示正确"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # Assert - 检查页面标题
    page_title = page.locator("h1, h2", has_text="All Products")
    expect(page_title.first).to_be_visible(timeout=5000)
    
    # 检查商品卡片
    products = page.locator("mat-card:has(button:has-text('Add to Basket')), .mat-card:has(button:has-text('Add to Basket'))")
    expect(products.first).to_be_visible(timeout=5000)
    
    # 验证至少有一个商品
    assert products.count() > 0, "页面上没有商品"


def test_product_card_fields(logged_in_page: Page):
    """测试商品卡片包含必要字段"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # 获取第一个商品卡片
    first_product = page.locator("mat-card:has(button:has-text('Add to Basket'))").first
    expect(first_product).to_be_visible(timeout=5000)
    
    # Assert - 检查商品卡片包含必要信息
    product_text = first_product.inner_text()
    
    # 检查价格信息（包含数字和货币符号）
    import re
    price_pattern = r'\d+\.?\d*\s*[€$]'  # 匹配价格格式
    assert re.search(price_pattern, product_text), f"商品卡片没有价格信息: {product_text}"
    
    # 检查商品名称
    assert len(product_text.strip()) > 0, "商品卡片内容为空"


def test_product_add_to_basket(logged_in_page: Page):
    """测试添加商品到购物车"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # 获取第一个商品的添加按钮
    add_button = page.locator("button:has-text('Add to Basket')").first
    expect(add_button).to_be_visible(timeout=5000)
    
    # 点击添加按钮
    add_button.click()
    page.wait_for_timeout(500)
    
    # Assert - 验证购物车数量增加
    cart_badge = page.locator("[aria-label*='Your Basket'] span, .mat-badge-content")
    if cart_badge.count() > 0:
        cart_count = cart_badge.first.inner_text()
        assert int(cart_count) >= 1, "购物车数量未增加"


def test_product_list_search(logged_in_page: Page):
    """测试商品列表搜索功能"""
    # Arrange
    page = logged_in_page
    
    # Act
    page.goto(f"{BASE_URL}/#/search")
    
    # 使用搜索框
    search_input = page.locator("input[placeholder*='Search' i]")
    if search_input.count() > 0:
        search_input.fill("Apple")
        search_input.press("Enter")
        page.wait_for_load_state("networkidle")
        
        # Assert
        products = page.locator("mat-card:has(button:has-text('Add to Basket'))")
        expect(products.first).to_be_visible(timeout=5000)
        
        # 验证搜索结果包含 Apple
        first_product_text = products.first.inner_text()
        assert "Apple" in first_product_text, f"搜索结果不包含 Apple: {first_product_text}"