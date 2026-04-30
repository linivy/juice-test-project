# test/rules/prompts.py

TEST_GENERATION_PROMPT = """
## 测试用例生成提示词

请根据以下规则生成 pytest + playwright 测试用例：

### 核心要求

1. 每个测试函数必须对应功能测试点ID（格式：TC-{MODULE}-{NUMBER}）
2. 函数文档字符串必须包含：测试目标、前置条件、测试步骤、预期结果
3. 参数化策略：≤5组用内联，6-10组用内联加注释，11-30组用外部JSON，>30组动态生成，共享数据用fixture
4. 必须包含allure元数据

### 当前任务

- 模块名称: {module_name}
- 功能名称: {feature_name}
- 功能测试点: {test_points}
- 测试数据: {test_data}

请生成测试用例代码。
"""


def get_prompt(module_name: str, feature_name: str, test_points: list, test_data: dict = None) -> str:
    test_points_str = "\n".join([f"   - {tp}" for tp in test_points])
    test_data_str = str(test_data) if test_data else "暂无"
    return TEST_GENERATION_PROMPT.format(
        module_name=module_name,
        feature_name=feature_name,
        test_points=test_points_str,
        test_data=test_data_str
    )


def get_login_prompt() -> str:
    return get_prompt(
        module_name="登录",
        feature_name="表单验证",
        test_points=[
            "TC-LOGIN-001: 登录页面加载",
            "TC-LOGIN-002: 有效凭据登录",
            "TC-LOGIN-003: 无效凭据登录",
        ],
        test_data={"users": [("admin", "123"), ("test", "456")]}
    )


if __name__ == "__main__":
    print(get_login_prompt())