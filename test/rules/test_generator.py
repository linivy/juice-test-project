# test/rules/test_generator.py
from parameterization_rules import ParameterizationRuleEngine
import inspect

class SmartTestGenerator:
    """智能测试生成器 - 根据数据特征自动选择策略"""
    
    def __init__(self):
        self.rule_engine = ParameterizationRuleEngine()
    
    def analyze_and_generate(self, test_data_config):
        """
        分析测试数据配置并生成相应的测试代码
        
        Args:
            test_data_config: {
                "test_name": "test_login_with_invalid_credentials",
                "params": ["email", "password", "expected_error"],
                "data": [...] 或 {"source": "file", "path": "data.json"} 等
            }
        """
        data = test_data_config["data"]
        
        # 判断数据类型和特征
        data_obj = self._create_data_object(data)
        
        # 决策策略
        strategy, template_func = self.rule_engine.decide_strategy(data_obj)
        
        # 生成相应代码
        if strategy == "inline":
            return template_func(
                test_data_config["test_name"],
                test_data_config["params"],
                data
            )
        elif strategy == "external":
            return template_func(
                test_data_config["test_name"],
                test_data_config["params"],
                data.get("file_path", "test_data.json")
            )
        elif strategy == "fixture":
            return template_func(
                test_data_config["test_name"],
                test_data_config["params"],
                f"{test_data_config['test_name']}_data"
            )
        elif strategy == "dynamic":
            return template_func(
                test_data_config["test_name"],
                test_data_config["params"],
                f"generate_{test_data_config['test_name']}_data"
            )
    
    def _create_data_object(self, data):
        """创建带元数据的数据对象"""
        class TestData:
            pass
        
        data_obj = TestData()
        
        if isinstance(data, list):
            data_obj.data = data
            data_obj.length = len(data)
            data_obj.shared = False
            data_obj.dynamic = False
        elif isinstance(data, dict):
            data_obj.data = data.get("data", [])
            data_obj.length = len(data_obj.data)
            data_obj.shared = data.get("shared", False)
            data_obj.dynamic = data.get("dynamic", False)
            if data.get("generator"):
                data_obj.generator = data["generator"]
        
        return data_obj

# 使用示例
generator = SmartTestGenerator()

# 场景1: 简单参数组合 (<10组)
simple_data = {
    "test_name": "test_login_basic",
    "params": ["username", "password", "expected"],
    "data": [
        ("admin", "123", "success"),
        ("user", "456", "fail"),
    ]
}
code1 = generator.analyze_and_generate(simple_data)

# 场景2: 参数组合较多 (>10组)
large_data = {
    "test_name": "test_login_massive",
    "params": ["email", "password", "error_msg"],
    "data": {
        "data": [],  # 实际会从文件读取
        "file_path": "test_data/large_login_data.json"
    }
}
code2 = generator.analyze_and_generate(large_data)

# 场景3: 多个测试共享同一组数据
shared_data = {
    "test_name": "test_login_shared",
    "params": ["user_type", "email", "password"],
    "data": {
        "data": [
            ("admin", "admin@test.com", "admin123"),
            ("user", "user@test.com", "user123"),
        ],
        "shared": True
    }
}
code3 = generator.analyze_and_generate(shared_data)

# 场景4: 需要动态生成数据
dynamic_data = {
    "test_name": "test_login_random",
    "params": ["random_email", "random_pwd", "expected"],
    "data": {
        "dynamic": True,
        "generator": "generate_random_credentials"
    }
}
code4 = generator.analyze_and_generate(dynamic_data)