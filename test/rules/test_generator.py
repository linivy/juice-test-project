# test/rules/test_generator.py
from parameterization_rules import ParameterizationRuleEngine, ParameterizationStrategy
import inspect

class SmartTestGenerator:
    """智能测试生成器 - 根据数据特征自动选择策略"""
    
    def __init__(self):
        self.rule_engine = ParameterizationRuleEngine()
    
    def _generate_inline_code(self, test_name, params, data):
        """生成内联参数化代码"""
        params_str = ", ".join(params)
        data_str = str(data).replace("'", '"')
        return f'''@pytest.mark.parametrize("{params_str}", {data_str})
def {test_name}({params_str}):
    """参数化测试 - {test_name}"""
    # 测试逻辑
    pass
'''
    
    def _generate_external_code(self, test_name, params, file_path):
        """生成外部文件参数化代码"""
        params_str = ", ".join(params)
        return f'''def load_test_data():
    import json
    with open("{file_path}", "r") as f:
        return json.load(f)

@pytest.mark.parametrize("{params_str}", load_test_data())
def {test_name}({params_str}):
    """参数化测试 - {test_name}"""
    # 测试逻辑
    pass
'''
    
    def _generate_fixture_code(self, test_name, params, fixture_name):
        """生成 fixture 参数化代码"""
        params_str = ", ".join(params)
        return f'''@pytest.fixture(params=[
    # 共享测试数据
])
def {fixture_name}(request):
    return request.param

def {test_name}({fixture_name}):
    """参数化测试 - {test_name}"""
    # 使用 fixture 数据
    pass
'''
    
    def _generate_dynamic_code(self, test_name, params, generator_name):
        """生成动态参数化代码"""
        params_str = ", ".join(params)
        return f'''def {generator_name}():
    """动态生成测试数据"""
    # 动态生成逻辑
    return []

@pytest.mark.parametrize("{params_str}", {generator_name}())
def {test_name}({params_str}):
    """参数化测试 - {test_name}"""
    # 测试逻辑
    pass
'''
    
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
        
        # 决策策略（返回枚举对象）
        strategy = self.rule_engine.decide_strategy(data_obj)
        
        # 生成相应代码（使用枚举值比较）
        if strategy == ParameterizationStrategy.INLINE:
            return self._generate_inline_code(
                test_data_config["test_name"],
                test_data_config["params"],
                data
            )
        elif strategy == ParameterizationStrategy.EXTERNAL_FILE:
            return self._generate_external_code(
                test_data_config["test_name"],
                test_data_config["params"],
                data.get("file_path", "test_data.json")
            )
        elif strategy == ParameterizationStrategy.FIXTURE_SHARED:
            return self._generate_fixture_code(
                test_data_config["test_name"],
                test_data_config["params"],
                f"{test_data_config['test_name']}_data"
            )
        elif strategy == ParameterizationStrategy.DYNAMIC:
            return self._generate_dynamic_code(
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
