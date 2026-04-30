# test/factories/data_factory.py
"""测试数据工厂 - 自动生成测试数据"""

import random
import string
from dataclasses import dataclass
from typing import List, Optional
from faker import Faker

fake = Faker("zh_CN")  # 中文数据


@dataclass
class UserData:
    """用户测试数据"""
    email: str
    password: str
    username: str
    phone: str
    address: str
    
    @classmethod
    def random(cls, password: str = "Test123456"):
        """生成随机用户数据"""
        name = fake.name()
        return cls(
            email=fake.email(),
            password=password,
            username=name,
            phone=fake.phone_number(),
            address=fake.address()
        )
    
    @classmethod
    def admin(cls):
        """管理员用户数据"""
        return cls(
            email="admin@juice-sh.op",
            password="admin123",
            username="管理员",
            phone="13800138000",
            address="北京市朝阳区"
        )


@dataclass
class ProductData:
    """商品测试数据"""
    name: str
    price: float
    category: str
    description: str
    stock: int
    
    @classmethod
    def random(cls):
        """生成随机商品数据"""
        return cls(
            name=fake.word() + " " + random.choice(["Juice", "Drink", "Snack"]),
            price=round(random.uniform(1.99, 99.99), 2),
            category=random.choice(["Beverages", "Snacks", "Fruits"]),
            description=fake.sentence(),
            stock=random.randint(0, 1000)
        )
    
    @classmethod
    def apple_juice(cls):
        """预设商品数据"""
        return cls(
            name="Apple Juice",
            price=1.99,
            category="Beverages",
            description="Fresh apple juice",
            stock=100
        )


@dataclass
class OrderData:
    """订单测试数据"""
    items: List[dict]
    total: float
    status: str
    shipping_address: str
    
    @classmethod
    def single_product(cls, product_name: str = "Apple Juice", quantity: int = 1, price: float = 1.99):
        """单商品订单"""
        total = price * quantity
        return cls(
            items=[{"name": product_name, "quantity": quantity, "price": price}],
            total=total,
            status="pending",
            shipping_address=fake.address()
        )
    
    @classmethod
    def multiple_products(cls):
        """多商品订单"""
        items = [
            {"name": "Apple Juice", "quantity": 2, "price": 1.99},
            {"name": "Orange Juice", "quantity": 1, "price": 2.99},
        ]
        total = sum(item["price"] * item["quantity"] for item in items)
        return cls(
            items=items,
            total=round(total, 2),
            status="pending",
            shipping_address=fake.address()
        )


@dataclass
class SearchData:
    """搜索测试数据"""
    keyword: str
    expected_result_count: int
    should_exist: bool


class TestDataFactory:
    """测试数据工厂 - 统一管理测试数据"""
    
    # 有效登录数据
    VALID_LOGINS = [
        ("admin@juice-sh.op", "admin123", "管理员"),
        ("jim@juice-sh.op", "ncc-1701", "普通用户"),
        ("bender@juice-sh.op", "OhG0dPlease1nsertLiquor!", "测试用户"),
    ]
    
    # 无效登录数据
    INVALID_LOGINS = [
        ("invalid@example.com", "wrongpassword", "Invalid email or password", "错误邮箱+错误密码"),
        ("", "admin123", "Email is required", "空邮箱+正确密码"),
        ("admin@juice-sh.op", "", "Password is required", "正确邮箱+空密码"),
        ("普通用户", "123456", "Invalid email or password", "无效邮箱格式"),
    ]
    
    # 边界值数据
    BOUNDARY_VALUES = {
        "email": [
            ("a@b.c", "最短邮箱"),
            ("a" * 50 + "@example.com", "超长邮箱"),
        ],
        "password": [
            ("1", "最短密码"),
            ("p" * 100, "超长密码"),
            ("!@#$%^&*()", "特殊字符"),
        ]
    }
    
    # 安全攻击数据
    SECURITY_ATTACKS = [
        ("' OR '1'='1", "anything", "SQL注入攻击"),
        ("<script>alert('xss')</script>", "password", "XSS攻击"),
        ("admin'--", "anything", "SQL注释注入"),
        ("'; DROP TABLE users;--", "password", "SQL删除注入"),
    ]
    
    # 搜索关键词
    SEARCH_KEYWORDS = [
        ("Apple", True, "存在的商品"),
        ("Juice", True, "存在的商品"),
        ("Fruit", True, "存在的商品"),
        ("NonExistentXYZ", False, "不存在的商品"),
        ("", True, "空字符串"),
    ]
    
    @classmethod
    def get_boundary_test_data(cls):
        """获取边界值测试数据（用于参数化）"""
        test_data = []
        
        # 邮箱边界值
        for email, desc in cls.BOUNDARY_VALUES["email"]:
            test_data.append((email, "password123", f"邮箱边界: {desc}"))
        
        # 密码边界值
        for password, desc in cls.BOUNDARY_VALUES["password"]:
            test_data.append(("test@test.com", password, f"密码边界: {desc}"))
        
        return test_data
    
    @classmethod
    def get_pagination_data(cls, page_size: int = 10):
        """获取分页测试数据"""
        return {
            "page": random.randint(1, 10),
            "size": page_size,
            "sort": random.choice(["asc", "desc"]),
        }
    
    @classmethod
    def generate_random_string(cls, length: int = 10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @classmethod
    def generate_random_email(cls):
        """生成随机邮箱"""
        return f"{cls.generate_random_string(8)}@test.com"
    
    @classmethod
    def generate_random_phone(cls):
        """生成随机手机号"""
        return f"1{random.choice(['3', '5', '7', '8', '9'])}{''.join(random.choices(string.digits, k=9))}"