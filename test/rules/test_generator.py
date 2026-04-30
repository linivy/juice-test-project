# test/rules/test_generator.py
"""
智能测试生成器 - 根据数据特征自动选择策略
"""

from parameterization_rules import ParameterizationRuleEngine, ParameterizationStrategy


class SmartTestGenerator:
    """智能测试生成器 - 根据数据特征自动选择策略"""
    
    def __init__(self):
        self.rule_engine = ParameterizationRuleEngine()
    
    def _generate_inline_code(self, test_name: str, params: list, data: list) -> str:
        """生成内联参数化代码"""
        params_str = ", ".join(params)
        # 格式化数据
        data_lines = []
        for item in data:
            if isinstance(item, tuple):
                data_lines.append(str(item))
            else:
                data_lines.append(str(item))
        
        data_str = ",\n        ".join(data_lines)
        
        return f'''
@pytest.mark.parametrize("{params_str}", [
        {data_str}
    ])
def {test_name}(self, {params_str}):
    """
    参数化测试 - 内联数据
    数据组数: {len(data)}
    """
    # TODO: 实现测试逻辑
    pass
'''
    
    def _generate_external_code(self, test_name: str, params: list, file_path: str) -> str:
        """生成外部文件参数化代码"""
        params_str = ", ".join(params)
        
        return f'''
import json
import os

def _load_{test_name}_data():
    """从JSON文件加载测试数据"""
    data_file = "{file_path}"
    if not os.path.exists(data_file):
        return []
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.parametrize("{params_str}", _load_{test_name}_data())
def {test_name}(self, {params_str}):
    """
    参数化测试 - 外部数据文件
    数据来源: {file_path}
    """
    # TODO: 实现测试逻辑
    pass
'''
    
    def _generate_fixture_code(self, test_name: str, params: list, fixture_name: str) -> str:
        """生成 fixture 参数化代码"""
        params_str = ", ".join(params)
        
        return f'''
@pytest.fixture(scope="module")
def {fixture_name}():
    """
    共享测试数据 Fixture
    对应功能测试点: {test_name}
    """
    return [
        # 每组数据格式: ({params_str})
        # 示例: ("admin@juice-sh.op", "admin123", "success"),
    ]

def {test_name}(self, {fixture_name}):
    """
    参数化测试 - 使用共享 Fixture
    数据来源: {fixture_name}
    """
    for data in {fixture_name}:
        # 解包数据
        {params_str} = data
        # TODO: 实现测试逻辑
        pass
'''
    
    def _generate_dynamic_code(self, test_name: str, params: list, generator_name: str) -> str:
        """生成动态参数化代码"""
        params_str = ", ".join(params)
        
        return f'''
import random
import string

def {generator_name}():
    """动态生成测试数据"""
    test_data = []
    for i in range(50):  # 动态生成50组数据
        email = f"test_{{i}}@example.com"
        password = ''.join(random.choices(string.ascii_letters, k=8))
        expected = "Invalid email or password"
        test_data.append((email, password, expected))
    return test_data

@pytest.mark.parametrize("{params_str}", {generator_name}())
def {test_name}(self, {params_str}):
    """
    参数化测试 - 动态生成数据
    说明: 测试数据在运行时动态生成
    """
    # TODO: 实现测试逻辑
    pass
'''
    
    def analyze_and_generate(self, test_data_config: dict) -> str:
        """
        分析测试数据配置并生成相应的测试代码
        
        Args:
            test_data_config: {
                "test_name": "test_login_with_invalid_credentials",
                "params": ["email", "password", "expected_error"],
                "data": [...] 或 {"data": [...], "shared": True} 等
            }
        
        Returns:
            生成的测试代码字符串
        """
        test_name = test_data_config["test_name"]
        params = test_data_config["params"]
        data = test_data_config["data"]
        
        # 创建数据对象
        data_obj = self._create_data_object(data)
        
        # 决策策略（现在返回的是枚举对象）
        strategy = self.rule_engine.decide_strategy(data_obj)
        
        # 根据策略生成代码（使用枚举值比较）
        if strategy == ParameterizationStrategy.INLINE:
            # 提取实际数据
            actual_data = data if isinstance(data, list) else data.get("data", [])
            return self._generate_inline_code(test_name, params, actual_data)
        
        elif strategy == ParameterizationStrategy.EXTERNAL_FILE:
            file_path = data.get("file_path", f"test-data/{test_name}.json")
            return self._generate_external_code(test_name, params, file_path)
        
        elif strategy == ParameterizationStrategy.FIXTURE_SHARED:
            fixture_name = f"{test_name}_data"
            return self._generate_fixture_code(test_name, params, fixture_name)
        
        elif strategy == ParameterizationStrategy.DYNAMIC:
            generator_name = data.get("generator", f"generate_{test_name}_data")
            return self._generate_dynamic_code(test_name, params, generator_name)
        
        else:
            # 默认使用内联
            actual_data = data if isinstance(data, list) else data.get("data", [])
            return self._generate_inline_code(test_name, params, actual_data)
    
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
        else:
            data_obj.data = []
            data_obj.length = 0
            data_obj.shared = False
            data_obj.dynamic = False
        
        return data_obj


# ==================== 使用示例 ====================

if __name__ == "__main__":
    generator = SmartTestGenerator()
    
    print("=" * 60)
    print("场景1: 内联策略（小数据集）")
    print("=" * 60)
    
    config1 = {
        "test_name": "test_login_inline",
        "params": ["email", "password", "expected"],
        "data": [
            ("admin", "123", "success"),
            ("user", "456", "fail"),
        ]
    }
    code1 = generator.analyze_and_generate(config1)
    print(code1)
    
    print("\n" + "=" * 60)
    print("场景2: 共享数据策略")
    print("=" * 60)
    
    config2 = {
        "test_name": "test_login_shared",
        "params": ["email", "password", "role"],
        "data": {
            "data": [
                ("admin@juice-sh.op", "admin123", "管理员"),
                ("jim@juice-sh.op", "ncc-1701", "普通用户"),
            ],
            "shared": True
        }
    }
    code2 = generator.analyze_and_generate(config2)
    print(code2)
    
    print("\n" + "=" * 60)
    print("场景3: 动态生成策略")
    print("=" * 60)
    
    config3 = {
        "test_name": "test_login_dynamic",
        "params": ["email", "password", "expected"],
        "data": {
            "dynamic": True,
            "generator": "generate_random_data"
        }
    }
    code3 = generator.analyze_and_generate(config3)
    print(code3)