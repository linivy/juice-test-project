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