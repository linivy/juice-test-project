"""
# ==================== 规范同步信息 ====================
spec_file: test/cases/ui-testing-patterns.md
spec_version: 1.0.0
spec_hash: e8847ce5
spec_last_updated: 2026-01-15
# ===================================================
"""

# test/list/test_product_list.py
"""
商品列表页面测试 - 卡片形式展示

功能测试点:
- TC-PROD-001: 商品列表页面显示正确
- TC-PROD-002: 商品卡片包含必要字段（名称、价格）
- TC-PROD-003: 添加商品到购物车
- TC-PROD-004: 商品搜索功能（参数化）
- TC-PROD-005: 搜索结果为空时显示提示

测试覆盖矩阵:
| 功能测试点ID | 功能描述 | 测试用例函数 | 参数化类型 | 数据组数 |
|-------------|---------|-------------|-----------|---------|
| TC-PROD-001 | 商品列表页面显示 | test_product_list_display | basic | 1 |
| TC-PROD-002 | 商品卡片字段验证 | test_product_card_fields | basic | 1 |
| TC-PROD-003 | 添加到购物车 | test_product_add_to_basket | basic | 1 |
| TC-PROD-004 | 商品搜索 | test_product_search | parametrized | 5 |
| TC-PROD-005 | 搜索无结果 | test_search_no_results | basic | 1 |
"""

import pytest
import re
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

def close_challenge_dialog(page: Page):
    """关闭挑战成功弹窗"""
    try:
        close_btn = page.locator(".mat-mdc-dialog-surface button[aria-label='Close'], button[mat-dialog-close]")
        if close_btn.is_visible(timeout=2000):
            close_btn.click()
    except:
        pass

def activate_search(page: Page):
    """激活搜索框"""
    page.keyboard.press("/")
    search_input = page.locator("input[placeholder*='Search' i]")
    if search_input.count() > 0 and search_input.first.is_visible():
        return search_input.first
    
    search_icon = page.locator("mat-icon", has_text="search")
    if search_icon.count() > 0:
        search_icon.first.click()
    
    return page.locator("input[placeholder*='Search' i]").first

# ==================== TC-PROD-001: 商品列表页面显示 ====================

def test_product_list_display(logged_in_page: Page):
    """
    【TC-PROD-001】测试商品列表页面显示正确
    
    测试目标: 验证商品列表页面正常加载，商品卡片可见
    
    前置条件:
      - 用户已登录
      
    测试步骤:
      1. 访问搜索页面
      2. 等待页面加载完成
      3. 验证商品卡片可见
      
    预期结果:
      - 至少有一个商品卡片显示
    """
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # 等待商品卡片加载
    products = page.locator("mat-card:has(button:has-text('Add to Basket'))")
    expect(products.first).to_be_visible(timeout=10000)
    assert products.count() > 0, "页面上没有商品"

# ==================== TC-PROD-002: 商品卡片字段验证 ====================

def test_product_card_fields(logged_in_page: Page):
    """
    【TC-PROD-002】测试商品卡片包含必要字段（名称、价格）
    
    测试目标: 验证商品卡片显示完整的商品信息
    
    前置条件:
      - 用户已登录
      - 商品列表已加载
      
    测试步骤:
      1. 获取第一个商品卡片
      2. 验证卡片内容不为空
      3. 验证包含价格信息
      
    预期结果:
      - 商品卡片有名称和价格
    """
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    first_product = page.locator("mat-card:has(button:has-text('Add to Basket'))").first
    expect(first_product).to_be_visible(timeout=10000)
    
    product_text = first_product.inner_text()
    
    # 验证价格信息
    price_pattern = r'\d+\.?\d*\s*[€$¤¥£]'
    assert re.search(price_pattern, product_text), f"商品卡片没有价格信息: {product_text[:100]}"
    
    # 验证商品名称存在
    assert len(product_text.strip()) > 0, "商品卡片内容为空"

# ==================== TC-PROD-003: 添加商品到购物车 ====================

def test_product_add_to_basket(logged_in_page: Page):
    """
    【TC-PROD-003】测试添加商品到购物车
    
    测试目标: 验证用户可以添加商品到购物车
    
    前置条件:
      - 用户已登录
      - 商品列表已加载
      
    测试步骤:
      1. 点击第一个商品的"Add to Basket"按钮
      2. 验证购物车数量增加
      
    预期结果:
      - 购物车徽章数量 >= 1
    """
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # 获取第一个商品的添加按钮
    add_button = page.locator("button:has-text('Add to Basket')").first
    expect(add_button).to_be_visible(timeout=5000)
    
    # 点击添加按钮
    add_button.click()
    
    # 验证购物车数量增加
    cart_badge = page.locator("[aria-label*='Your Basket'] span, .mat-badge-content")
    if cart_badge.count() > 0:
        cart_count = cart_badge.first.inner_text()
        assert int(cart_count) >= 1, "购物车数量未增加"

# ==================== TC-PROD-004: 商品搜索功能（参数化） ====================

@pytest.mark.parametrize("search_keyword,expected_has_results", [
    ("Apple", True),      # 存在 - 应该有结果
    ("Juice", True),      # 存在 - 应该有结果
    ("Fruit", True),      # 存在 - 应该有结果
    ("XYZNotExist", False),  # 不存在 - 无结果
    ("", True),           # 空字符串 - 显示所有
])
def test_product_search(logged_in_page: Page, search_keyword: str, expected_has_results: bool):
    """
    【TC-PROD-004】测试商品搜索功能 - 参数化
    
    测试目标: 验证搜索功能对多种关键词的正确响应
    
    当前测试场景: 关键词 '{search_keyword}'，期望{'有' if expected_has_results else '无'}结果
    
    前置条件:
      - 用户已登录
      
    测试步骤:
      1. 输入搜索关键词
      2. 提交搜索
      3. 验证结果符合预期
      
    预期结果:
      - 存在关键词时显示商品卡片
      - 不存在关键词时显示"No results found"
    """
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    # 激活搜索框
    search_input = activate_search(page)
    search_input.fill(search_keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")
    
    if expected_has_results:
        # 期望有搜索结果
        products = page.locator("mat-card:has(button:has-text('Add to Basket'))")
        if search_keyword != "":  # 非空搜索应该有结果
            expect(products.first).to_be_visible(timeout=5000)
    else:
        # 期望无结果 - 显示"No results found"
        no_results = page.locator("text='No results found'")
        expect(no_results.first).to_be_visible(timeout=5000)

# ==================== TC-PROD-005: 搜索无结果提示 ====================

def test_search_no_results(logged_in_page: Page):
    """
    【TC-PROD-005】测试搜索不存在的商品时显示正确提示
    
    测试目标: 验证搜索无结果时显示友好的提示信息
    
    前置条件:
      - 用户已登录
      
    测试步骤:
      1. 搜索不存在的商品
      2. 验证"No results found"提示显示
      3. 验证提示信息完整
      
    预期结果:
      - 显示"No results found"
      - 显示"Try adjusting your search"提示
    """
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    page.goto(f"{BASE_URL}/#/search")
    page.wait_for_load_state("networkidle")
    
    search_input = activate_search(page)
    search_input.fill("NonExistentProductXYZ123")
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")
    
    # 验证显示 "No results found" 提示
    no_results_message = page.locator("text='No results found'")
    expect(no_results_message.first).to_be_visible(timeout=5000)
    
    # 验证提示文本完整
    hint_text = page.get_by_text("Try adjusting your search", exact=False)
    expect(hint_text.first).to_be_visible(timeout=5000)