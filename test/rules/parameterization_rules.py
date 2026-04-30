# test/rules/parameterization_rules.py
"""
参数化策略决策规则
根据数据特征自动选择最优实现方式
"""

from typing import List, Tuple, Any, Union
from enum import Enum


class ParameterizationStrategy(Enum):
    """参数化策略枚举"""
    INLINE = "inline"           # 直接在装饰器中硬编码
    EXTERNAL_FILE = "external"  # 外部文件存储
    FIXTURE_SHARED = "fixture"  # pytest fixture 共享数据
    DYNAMIC = "dynamic"         # 动态生成数据


class ParameterizationRuleEngine:
    """参数化规则引擎"""
    
    def __init__(self):
        self.rules = [
            {
                "name": "simple_inline_rule",
                "condition": self._is_small_inline,
                "strategy": ParameterizationStrategy.INLINE
            },
            {
                "name": "shared_data_rule", 
                "condition": self._is_shared_fixture,
                "strategy": ParameterizationStrategy.FIXTURE_SHARED
            },
            {
                "name": "external_file_rule",
                "condition": self._is_external_data,
                "strategy": ParameterizationStrategy.EXTERNAL_FILE
            },
            {
                "name": "dynamic_data_rule",
                "condition": self._is_dynamic_large,
                "strategy": ParameterizationStrategy.DYNAMIC
            }
        ]
    
    def _get_data_length(self, data: Any) -> int:
        """获取数据长度"""
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict):
            return len(data.get("data", []))
        return 0
    
    def _has_flag(self, data: Any, flag_name: str) -> bool:
        """检查是否包含特定标志"""
        if isinstance(data, dict):
            return data.get(flag_name, False)
        return False
    
    def _is_small_inline(self, data: Any) -> bool:
        """小数据集 - 使用内联"""
        length = self._get_data_length(data)
        return length <= 10 and not self._has_flag(data, "shared")
    
    def _is_shared_fixture(self, data: Any) -> bool:
        """共享数据 - 使用 fixture"""
        return self._has_flag(data, "shared") and self._get_data_length(data) <= 50
    
    def _is_external_data(self, data: Any) -> bool:
        """中等数据 - 使用外部文件"""
        length = self._get_data_length(data)
        return 10 < length <= 30 and not self._has_flag(data, "dynamic")
    
    def _is_dynamic_large(self, data: Any) -> bool:
        """大数据或动态数据 - 使用动态生成"""
        length = self._get_data_length(data)
        return length > 30 or self._has_flag(data, "dynamic")
    
    def decide_strategy(self, test_data: Any) -> ParameterizationStrategy:
        """决策使用哪种策略"""
        for rule in self.rules:
            if rule["condition"](test_data):
                print(f"📊 数据特征: 数量={self._get_data_length(test_data)}")
                print(f"🎯 选择策略: {rule['strategy'].value}")
                return rule["strategy"]
        
        return ParameterizationStrategy.INLINE


# 辅助函数：判断数据特征
def analyze_test_data(data: Union[List, dict]) -> dict:
    """分析测试数据特征"""
    if isinstance(data, list):
        return {
            "type": "list",
            "length": len(data),
            "shared": False,
            "dynamic": False
        }
    elif isinstance(data, dict):
        inner_data = data.get("data", [])
        return {
            "type": "dict",
            "length": len(inner_data),
            "shared": data.get("shared", False),
            "dynamic": data.get("dynamic", False),
            "file_path": data.get("file_path", ""),
            "generator": data.get("generator", "")
        }
    return {"type": "unknown", "length": 0}


# 使用示例
if __name__ == "__main__":
    engine = ParameterizationRuleEngine()
    
    # 测试1: 小数据集
    small_data = [("a", "b"), ("c", "d")]
    strategy = engine.decide_strategy(small_data)
    print(f"小数据集策略: {strategy.value}")  # 输出: inline
    
    # 测试2: 共享数据
    shared_data = {"data": [("a", "b")], "shared": True}
    strategy = engine.decide_strategy(shared_data)
    print(f"共享数据策略: {strategy.value}")  # 输出: fixture