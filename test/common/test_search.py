import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"


def activate_search(page: Page):
    """激活搜索功能 - 按 / 键或点击搜索图标"""
    # 尝试按 / 键激活搜索
    page.keyboard.press("/")
    page.wait_for_timeout(500)
    
    # 检查是否有搜索框变为可见
    search_input = page.locator("input[placeholder*='Search' i], input[placeholder*='search' i]")
    if search_input.count() > 0 and search_input.first.is_visible():
        return search_input.first
    
    # 如果按键无效，尝试点击搜索图标
    search_icon = page.locator("mat-icon", has_text="search")
    if search_icon.count() > 0 and search_icon.first.is_visible():
        search_icon.first.click()
        page.wait_for_timeout(500)
        
        # 再次查找搜索框
        search_input = page.locator("input[placeholder*='Search' i], input[placeholder*='search' i]")
        if search_input.count() > 0:
            return search_input.first
    
    # 最后的后备方案
    return page.locator("input").first


def close_cookie_banner(page: Page):
    """关闭 Cookie 弹窗"""
    try:
        cookie_btn = page.get_by_role("button", name="Me want it!")
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()
            page.wait_for_timeout(500)
    except:
        pass


def close_challenge_dialog(page: Page):
    """关闭挑战成功弹窗"""
    try:
        close_btn = page.locator(".mat-mdc-dialog-surface button[aria-label='Close'], .mat-dialog-actions button")
        if close_btn.is_visible(timeout=2000):
            close_btn.click()
            page.wait_for_timeout(500)
    except:
        pass


def test_search_exact_match(logged_in_page: Page):
    """搜索存在的商品 - 精确匹配"""
    # Arrange
    page = logged_in_page
    close_cookie_banner(page)
    close_challenge_dialog(page)
    
    # Act
    search_input = activate_search(page)
    search_input.fill("Apple Juice")
    search_input.press("Enter")
    
    # Assert
    page.wait_for_timeout(2000)
    close_challenge_dialog(page)  # 搜索后可能出现新的挑战弹窗
    
    # 使用更精确的商品卡片选择器，排除挑战消息
    products = page.locator("mat-card, .mat-card, div[class*='card'][class*='product']")
    expect(products.first).to_be_visible(timeout=10000)
    expect(products.first).to_contain_text("Apple Juice")


def test_search_partial_match(logged_in_page: Page):
    """搜索商品 - 部分匹配"""
    # Arrange
    page = logged_in_page
    close_cookie_banner(page)
    
    # Act
    search_input = activate_search(page)
    search_input.fill("Apple")
    search_input.press("Enter")
    
    # Assert
    page.wait_for_timeout(2000)
    products = page.locator("div[class*='card'], article, [class*='product']")
    expect(products.first).to_be_visible(timeout=10000)
    assert products.count() >= 1


def test_search_no_match(logged_in_page: Page):
    """搜索不存在的商品 - 验证显示 'No results found' 提示"""
    # Arrange
    page = logged_in_page
    close_cookie_banner(page)
    
    # Act
    search_input = activate_search(page)
    search_input.fill("NonExistentProductXYZ123")
    search_input.press("Enter")
    
    # Assert
    page.wait_for_timeout(2000)
    
    # 验证显示 "No results found" 提示
    no_results_message = page.locator("text='No results found'", has_text="No results found")
    expect(no_results_message.first).to_be_visible(timeout=5000)
    
    # 验证提示文本完整（使用 get_by_text 方法）
    hint_text = page.get_by_text("Try adjusting your search", exact=False)
    expect(hint_text.first).to_be_visible(timeout=5000)


def test_search_empty_string(logged_in_page: Page):
    """搜索空字符串 - 应显示所有商品"""
    # Arrange
    page = logged_in_page
    close_cookie_banner(page)
    
    # Act
    search_input = activate_search(page)
    
    # 先搜索一个商品
    search_input.fill("Apple")
    search_input.press("Enter")
    page.wait_for_timeout(1000)
    
    # 清空搜索框
    search_input.fill("")
    search_input.press("Enter")
    
    # Assert
    page.wait_for_timeout(2000)
    products = page.locator("div[class*='card'], article, [class*='product']")
    expect(products.first).to_be_visible(timeout=10000)
    assert products.count() > 0