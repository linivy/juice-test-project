"""
# ==================== 规范同步信息 ====================
spec_file: test/cases/ui-testing-patterns.md
spec_version: 1.0.0
spec_hash: e8847ce5
spec_last_updated: 2026-01-15
# ===================================================
"""

# test/data/test_data.py
TEST_USERS = [
    {"username": "admin", "password": "admin123", "expected": "success"},
    {"username": "test", "password": "wrong", "expected": "error"},
    {"username": "", "password": "", "expected": "error"},
]

TEST_PRODUCTS = [
    {"name": "Apple Juice", "price": 1.99, "category": "beverage"},
    {"name": "Orange Juice", "price": 1.99, "category": "beverage"},
]