import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"

def login(page: Page):
    """登录 Juice Shop"""
    page.goto(f"{BASE_URL}/#/login")
    page.wait_for_load_state("networkidle")
    
    page.fill("#email", "admin@juice-sh.op")
    page.fill("#password", "admin123")
    page.click("#loginButton")
    
    # 等待登录完成
    page.wait_for_url(f"{BASE_URL}/#/search", timeout=10000)


def test_search_exact_match(page: Page):
    """搜索存在的商品 - 精确匹配"""
    login(page)  # 先登录
    
    # 现在搜索框应该出现了
    search_input = page.locator("input[placeholder*='Search']")
    search_input.wait_for(state="visible", timeout=10000)
    
    search_input.fill("Apple Juice")
    search_input.press("Enter")
    
    page.wait_for_timeout(2000)
    
    products = page.locator(".mat-card-content")
    assert products.count() >= 1
    expect(products.first).to_contain_text("Apple Juice")