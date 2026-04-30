# test/rules/prompts.py
"""
测试用例生成提示词模板
用于 AI 辅助生成测试用例

支持三种页面类型的测试：
- form: 表单页面测试
- detail: 详情页面测试
- list: 列表页面测试
"""

TEST_GENERATION_PROMPT = """
## 测试用例生成提示词

请根据以下规则生成 pytest + playwright 测试用例：

### 页面类型判断

首先判断要测试的页面类型：
- **form**: 表单页面（登录、注册、创建、编辑等）
- **detail**: 详情页面（查看详情、订单详情等）
- **list**: 列表页面（订单列表、商品列表等）

### 核心要求（必须遵守）

1. **可追溯性**
   - 每个测试函数必须对应一个功能测试点ID
   - 格式：TC-{MODULE}-{NUMBER}（form）、TC-{MODULE}D-{NUMBER}（detail）、TC-{MODULE}L-{NUMBER}（list）
   - 函数文档字符串必须包含：【功能测试点ID】、测试目标、测试步骤、预期结果
   - 文件头部必须包含测试覆盖矩阵

2. **命名规范**
   - 基础功能测试：`test_{feature}_{test_point_id_lower}`
   - 参数化测试：`test_{feature}_param_{test_point_id_lower}`
   - 边界测试：`test_{feature}_boundary_{condition}`

3. **参数化策略**
   - ≤5组数据：使用内联参数化，每组数据必须包含场景描述
   - 6-10组数据：使用内联参数化，必须有详细的场景注释
   - 11-30组数据：使用外部JSON文件
   - >30组数据：动态生成
   - 多测试共享数据：使用fixture

4. **页面类型特定测试点**

### 表单页面 (form) 必须包含的测试点：
- TC-XXX-001: 页面正常加载
- TC-XXX-002: 有效数据提交成功
- TC-XXX-003: 无效数据提交失败（参数化）
- TC-XXX-004: 必填项验证
- TC-XXX-005: 边界值测试（参数化）
- TC-XXX-006: 多次重复提交测试
- TC-XXX-007: 表单重置功能测试
- TC-XXX-008: 特殊字符/SQL注入测试

### 详情页面 (detail) 必须包含的测试点：
- TC-XXXD-001: 详情页所有字段正确显示
- TC-XXXD-002: 可选字段为空时的显示
- TC-XXXD-003: 返回按钮功能
- TC-XXXD-004: 状态显示正确
- TC-XXXD-005: 详情页与列表页数据一致性
- TC-XXXD-006: 编辑按钮跳转功能
- TC-XXXD-007: 详情页加载

### 列表页面 (list) 必须包含的测试点：
- TC-XXXL-001: 列表页面正常加载
- TC-XXXL-002: 列表显示必要字段
- TC-XXXL-003: 导航栏访问
- TC-XXXL-004: 空列表显示提示
- TC-XXXL-005: 搜索功能（参数化）
- TC-XXXL-006: 排序功能
- TC-XXXL-007: 分页功能
- TC-XXXL-008: 新增后刷新
- TC-XXXL-009: 编辑后刷新
- TC-XXXL-010: 删除后刷新

### 当前任务信息

- 页面类型: {page_type}
- 模块名称: {module_name}
- 功能名称: {feature_name}
- 功能测试点: {test_points}
- 测试数据: {test_data}

请生成符合规范的测试用例代码。
"""


def get_test_generation_prompt(
    page_type: str,
    module_name: str,
    feature_name: str,
    test_points: list,
    test_data: dict = None
) -> str:
    """
    获取填充后的提示词

    Args:
        page_type: 页面类型 - "form", "detail", "list"
        module_name: 模块名称，如"登录"
        feature_name: 功能名称，如"表单验证"
        test_points: 功能测试点列表
        test_data: 测试数据字典
    """
    test_points_str = "\n".join([f"   - {tp}" for tp in test_points])
    
    test_data_str = "暂无"
    if test_data:
        import json
        test_data_str = json.dumps(test_data, ensure_ascii=False, indent=2)
    
    return TEST_GENERATION_PROMPT.format(
        page_type=page_type,
        module_name=module_name,
        feature_name=feature_name,
        test_points=test_points_str,
        test_data=test_data_str
    )


# ==================== 快捷方法 ====================

def get_form_prompt(module_name: str, feature_name: str, test_data: dict = None) -> str:
    """获取表单页面的测试提示词"""
    test_points = [
        f"TC-{module_name.upper()}-001: {feature_name}页面正常加载",
        f"TC-{module_name.upper()}-002: 有效数据提交成功",
        f"TC-{module_name.upper()}-003: 无效数据提交失败（参数化）",
        f"TC-{module_name.upper()}-004: 必填项验证",
        f"TC-{module_name.upper()}-005: 边界值测试（参数化）",
        f"TC-{module_name.upper()}-006: 多次重复提交测试",
        f"TC-{module_name.upper()}-007: 表单重置功能测试",
        f"TC-{module_name.upper()}-008: 特殊字符/SQL注入测试",
    ]
    return get_test_generation_prompt("form", module_name, feature_name, test_points, test_data)


def get_detail_prompt(module_name: str, feature_name: str, test_data: dict = None) -> str:
    """获取详情页面的测试提示词"""
    test_points = [
        f"TC-{module_name.upper()}D-001: {feature_name}详情页所有字段正确显示",
        f"TC-{module_name.upper()}D-002: 可选字段为空时的显示",
        f"TC-{module_name.upper()}D-003: 返回按钮功能",
        f"TC-{module_name.upper()}D-004: 状态显示正确",
        f"TC-{module_name.upper()}D-005: 详情页与列表页数据一致性",
        f"TC-{module_name.upper()}D-006: 编辑按钮跳转功能",
        f"TC-{module_name.upper()}D-007: {feature_name}详情页加载",
    ]
    return get_test_generation_prompt("detail", module_name, feature_name, test_points, test_data)


def get_list_prompt(module_name: str, feature_name: str, test_data: dict = None) -> str:
    """获取列表页面的测试提示词"""
    test_points = [
        f"TC-{module_name.upper()}L-001: {feature_name}列表页面正常加载",
        f"TC-{module_name.upper()}L-002: {feature_name}列表显示必要字段",
        f"TC-{module_name.upper()}L-003: 通过导航栏访问{feature_name}列表页",
        f"TC-{module_name.upper()}L-004: 空列表显示提示信息",
        f"TC-{module_name.upper()}L-005: {feature_name}列表搜索功能",
        f"TC-{module_name.upper()}L-006: {feature_name}列表排序功能",
        f"TC-{module_name.upper()}L-007: {feature_name}列表分页功能",
        f"TC-{module_name.upper()}L-008: 新增后列表刷新",
        f"TC-{module_name.upper()}L-009: 编辑后列表刷新",
        f"TC-{module_name.upper()}L-010: 删除后列表刷新",
    ]
    return get_test_generation_prompt("list", module_name, feature_name, test_points, test_data)


def get_login_prompt() -> str:
    """获取登录模块的测试提示词（表单类型）"""
    return get_form_prompt(
        module_name="LOGIN",
        feature_name="登录",
        test_data={
            "valid_users": [
                {"email": "admin@juice-sh.op", "password": "admin123"},
                {"email": "jim@juice-sh.op", "password": "ncc-1701"},
            ],
            "invalid_credentials": [
                {"email": "invalid@test.com", "password": "wrong", "expected_error": "Invalid email or password"},
                {"email": "", "password": "admin123", "expected_error": "Email is required"},
                {"email": "admin@juice-sh.op", "password": "", "expected_error": "Password is required"},
            ],
            "boundary_values": [
                {"email": "a@b.c", "boundary_type": "最短邮箱"},
                {"email": "a" * 50 + "@example.com", "boundary_type": "超长邮箱"},
                {"password": "1", "boundary_type": "最短密码"},
                {"password": "!" * 100, "boundary_type": "超长密码"},
            ],
            "security_tests": [
                {"attack": "' OR '1'='1", "type": "SQL注入"},
                {"attack": "<script>alert('xss')</script>", "type": "XSS攻击"},
            ]
        }
    )


if __name__ == "__main__":
    print("=" * 60)
    print("表单页面测试提示词示例")
    print("=" * 60)
    print(get_login_prompt())
    
    print("\n" + "=" * 60)
    print("详情页面测试提示词示例")
    print("=" * 60)
    print(get_detail_prompt("ORDER", "订单"))
    
    print("\n" + "=" * 60)
    print("列表页面测试提示词示例")
    print("=" * 60)
    print(get_list_prompt("PRODUCT", "商品"))