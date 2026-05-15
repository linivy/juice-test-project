# test/ai/prompt_constants.py
"""AI 测试生成器的 Prompt 常量定义"""


# ==================== 系统提示词 ====================
SYSTEM_PROMPT = (
    "你是测试自动化专家。输出要求：\n"
    "- 只输出测试方法代码，不要输出任何解释\n"
    "- 使用同步 def，不要用 async\n"
    "- 使用 @allure.title，不要用 @allure.it\n"
    "- 使用 page.fill，不要用 name_fill\n"
    "- 方法体内部统一缩进 8 个空格\n"
)


# ==================== 基础操作流程 ====================
def get_base_flow(context: dict) -> str:
    return (
        "\n## 页面操作流程（必须遵守）\n"
        "1. self.navigate_to_page(page)\n"
        '2. page.click("{btn_create}")\n'
        '3. page.wait_for_selector("{create_modal}", state="visible")\n'
        "4. 填写表单\n"
        '5. page.click("{btn_submit}") 或 page.click("{btn_save_draft}")\n'
    ).format(**context)


# ==================== 日期选择器处理 ====================
def get_date_picker_hint(context: dict) -> str:
    return (
        "\n## 日期选择器处理\n"
        "{form_start_time} 和 {form_end_time} 是只读的，必须用 JavaScript：\n"
        "    page.evaluate(\"document.querySelector('{form_start_time}').value = '2024-01-01 10:00';\")\n"
        "    page.evaluate(\"document.querySelector('{form_end_time}').value = '2024-01-01 18:00';\")\n"
    ).format(**context)


# ==================== 断言语法 ====================
def get_assertion_hint(context: dict) -> str:
    return (
        "\n## 断言语法\n"
        '    expect(page.locator("{toast}")).to_contain_text("成功")\n'
        '    expect(page.locator("{toast}")).to_be_visible()\n'
    ).format(**context)


# ==================== 输出格式要求 ====================
OUTPUT_FORMAT = (
    "\n## 输出格式要求\n"
    "- 不要使用 async def\n"
    "- 不要使用 @pytest.mark.asyncio\n"
    "- 不要使用 @allure.it，使用 @allure.title\n"
    "- 只输出方法代码\n"
)


# ==================== 子类型下拉框规则 ====================
def get_sub_type_rule(context: dict) -> str:
    return (
        "\n## 重要：表单字段的可见性规则\n"
        "\n"
        "### 子类型下拉框\n"
        "- 默认不可见\n"
        "- **必须先选择活动类型** (`{form_type}`) 才会显示\n"
        "- 示例：\n"
        "```python\n"
        'page.select_option("{form_type}", "社区活动")\n'
        'page.wait_for_selector("#subTypeDiv", state="visible")\n'
        'page.select_option("{form_sub_type}", "运动会")\n'
        "```\n"
    ).format(**context)


# ==================== Toast 消息说明 ====================
TOAST_HINT = (
    "\n### Toast 消息说明\n"
    "- ✅ 操作成功时：会显示 toast 消息\n"
    "- ✅ 表单验证失败时：也会显示 toast 消息，同时显示内联错误提示\n"
)


# ==================== 错误提示元素 ====================
ERROR_ELEMENTS = (
    "\n### 常见错误提示元素\n"
    "- 活动名称错误：`#error_formName`\n"
    "- 活动类型错误：`#error_formType`\n"
    "- 开始时间错误：`#error_formStartTime`\n"
    "- 结束时间错误：`#error_formEndTime`\n"
    "- 时间范围错误：`#error_errorTimeRange`\n"
)


# ==================== 省市区级联规则 ====================
def get_cascade_rule(context: dict) -> str:
    return (
        "\n## 省市区级联规则\n"
        "- 必须先选择省份，城市的选项才会加载\n"
        "- 必须先选择城市，区县的选项才会加载\n"
        "- 示例：\n"
        "```python\n"
        'page.select_option("{form_province}", "广东省")\n'
        'page.wait_for_selector("{form_city} option:not([value=\'\'])", state="visible")\n'
        'page.select_option("{form_city}", "深圳市")\n'
        'page.wait_for_selector("{form_district} option", state="visible")\n'
        'page.select_option("{form_district}", "南山区")\n'
        "```\n"
    ).format(**context)


# ==================== 确认弹框规则 ====================
def get_confirm_modal_rule(context: dict) -> str:
    return (
        "\n## 确认弹框显示条件\n"
        "\n"
        "- **确认弹框 (`{confirm_modal}`) 只在以下情况出现：**\n"
        "  - 所有必填字段都填写完整且验证通过时\n"
        "  - 表单**没有**任何验证错误时\n"
        "- **验证失败时不会弹出确认弹框**，而是直接显示 toast 错误消息\n"
        "- 因此：\n"
        "  - 测试正向成功流程时，**需要**等待确认弹框并点击确认\n"
        "  - 测试表单验证失败的场景时，**不要**等待确认弹框\n"
        "\n"
        "### 取消弹框 (`{cancel_modal}`)\n"
        "- 点击【放弃创建】按钮 (`{btn_cancel}`) 时会显示\n"
        "- 按钮说明：\n"
        "  - 确认放弃：点击 `{btn_confirm}`（确认弹框中的确定按钮）\n"
        "  - 取消放弃：点击 `{btn_cancel}` 或弹框中的取消按钮\n"
        "\n"
        "正向成功流程示例（会弹出确认弹框）：\n"
        "```python\n"
        "# 填写所有必填字段后提交\n"
        "page.fill(\"{form_name}\", \"测试活动\")\n"
        "page.select_option(\"{form_type}\", \"社区活动\")\n"
        "page.wait_for_selector(\"#subTypeDiv\", state=\"visible\")\n"
        "page.select_option(\"{form_sub_type}\", \"运动会\")\n"
        "page.evaluate(\"document.querySelector('{form_start_time}').value = '2024-01-01 10:00';\")\n"
        "page.evaluate(\"document.querySelector('{form_end_time}').value = '2024-01-01 18:00';\")\n"
        "page.fill(\"{form_description}\", \"这是一个测试活动\")\n"
        "page.click(\"{btn_submit}\")\n"
        "# 等待确认弹框\n"
        "page.wait_for_selector(\"{confirm_modal}\", state=\"visible\")\n"
        "page.click(\"{btn_confirm}\")\n"
        "self.wait_for_toast(page)\n"
        "expect(page.locator(\"{toast}\")).to_contain_text(\"{success_create}\")\n"
        "```\n"
        "\n"
        "验证失败示例（不会弹出确认弹框，直接显示错误）：\n"
        "```python\n"
        "# 活动名称为空，其他字段完整\n"
        "page.select_option(\"{form_type}\", \"社区活动\")\n"
        "page.wait_for_selector(\"#subTypeDiv\", state=\"visible\")\n"
        "page.select_option(\"{form_sub_type}\", \"运动会\")\n"
        "page.evaluate(\"document.querySelector('{form_start_time}').value = '2024-01-01 10:00';\")\n"
        "page.evaluate(\"document.querySelector('{form_end_time}').value = '2024-01-01 18:00';\")\n"
        "page.fill(\"{form_description}\", \"这是一个测试活动\")\n"
        "page.click(\"{btn_submit}\")\n"
        "# 验证错误 toast（不要等待确认弹框）\n"
        "expect(page.locator(\"{toast}\")).to_contain_text(\"{error_empty_name}\")\n"
        "expect(page.locator(\"#error_formName\")).to_be_visible()\n"
        "```\n"
    ).format(**context)


# ==================== 保存草稿说明 ====================
def get_draft_hint(context: dict) -> str:
    return (
        "\n## 活动保存草稿说明\n"
        "- 点击【保存草稿】按钮 (`{btn_save_draft}`) 时：\n"
        "  - 只验证必填字段（活动名称、活动类型）\n"
        "  - **不会验证**活动时间、活动简介等非必填字段\n"
        "  - 保存后状态为\"活动待提交\"\n"
        "  - 不会弹出确认弹框\n"
        "  - 验证失败时会显示具体的 toast 错误消息\n"
    ).format(**context)


# ==================== 提交创建说明 ====================
# test/ai/prompt_constants.py

def get_submit_hint(context: dict) -> str:
    required_fields_str = ', '.join(context.get('required_for_submit', []))
    
    # 从 context 中获取错误消息配置和字段标签
    error_msgs = context.get('error_messages', {})
    field_labels = context.get('field_labels', {})
    
    # 定义字段与错误消息的映射关系（从配置读取）
    field_error_configs = context.get('field_error_configs', [
        ('form_name', 'empty_name', field_labels.get('form_name', '字段')),
        ('form_type', 'empty_type', field_labels.get('form_type', '字段')),
        ('form_start_time', 'empty_start_time', field_labels.get('form_start_time', '字段')),
        ('form_end_time', 'empty_end_time', field_labels.get('form_end_time', '字段')),
        ('form_description', 'empty_description', field_labels.get('form_description', '字段')),
    ])
    
    # 动态构建错误消息示例
    error_examples = []
    for field_name, error_key, field_label in field_error_configs:
        if error_key in error_msgs:
            error_msg = error_msgs[error_key]
            error_examples.append(f'    - {field_label}为空 → "{error_msg}"')
    
    error_examples_str = '\n'.join(error_examples) if error_examples else '    - （根据项目配置定义）'
    
    return (
        "\n## 活动提交完成创建说明\n"
        "- 点击【完成创建】按钮 (`{btn_submit}`) 时：\n"
        f"  - 验证所有必填字段（{required_fields_str}）\n"
        "  - **验证通过后**才会弹出确认弹框 `{confirm_modal}`\n"
        "  - **验证失败时**不会弹出确认弹框，而是直接显示具体的 toast 错误消息\n"
        f"  - 错误消息示例（根据当前项目配置）：\n{error_examples_str}\n"
        "  - 同时会显示字段内联错误提示（如 `#error_formName`）\n"
        "  - **重要**：测试断言必须使用配置中定义的错误消息，而非测试点描述中的通用消息\n"
        "  - 点击确认后创建成功，显示 toast `{success_create}`\n"
    ).format(**context)


# ==================== 关键要点总结 ====================
KEY_POINTS = (
    "\n## 关键要点总结（再次强调）\n"
    "1. 子类型字段：必须先选活动类型，等待 `#subTypeDiv` 可见\n"
    "2. 省市区级联：必须按顺序选择，并等待下一级选项加载\n"
    "3. 文件上传：使用 `page.set_input_files(\"input[type='file']\", \"test.pdf\")`\n"
    "4. 错误消息：检查**具体字段错误**（如\"请输入活动名称\"），不是通用的\"活动信息未完善\"\n"
    "5. 确认弹框：**只在正向成功流程中等待**，验证失败时不要等待\n"
    "6. 保存草稿：只验证活动名称和活动类型\n"
    "7. 级联等待：使用 `page.wait_for_selector(\"#formCity option:not([value=''])\", state=\"visible\")` 等待非空选项\n"
    "8. 断言优先级：测试点描述中的错误消息仅供参考，**必须使用配置文件中定义的具体错误消息**（如配置中的 empty_name、empty_type 等）\n"
)


# ==================== 示例代码 ====================
def get_success_example(context: dict) -> str:
    # 从 context 获取示例数据
    example_data = context.get('example_data', {})
    activity_name = example_data.get('activity_name', '测试活动')
    activity_type = example_data.get('activity_type', '社区活动')
    sub_type = example_data.get('sub_type', '运动会')
    online_platform = example_data.get('online_platform', '腾讯会议')
    
    return (
        "\n## 示例：测试创建活动成功\n"
        "```python\n"
        '@allure.feature("{feature_name}")\n'
        '@allure.title("{tc_id}: 测试创建活动成功")\n'
        "def {method_name}(self, page):\n"
        "    self.navigate_to_page(page)\n"
        '    page.click("{btn_create}")\n'
        '    page.wait_for_selector("{create_modal}", state="visible")\n'
        f'    page.fill("{form_name}", "{activity_name}")\n'
        f'    page.select_option("{form_type}", "{activity_type}")\n'
        '    page.wait_for_selector("#subTypeDiv", state="visible")\n'
        f'    page.select_option("{form_sub_type}", "{sub_type}")\n'
        '    page.evaluate("document.querySelector(\'{form_start_time}\').value = \'2024-01-01 10:00\';")\n'
        '    page.evaluate("document.querySelector(\'{form_end_time}\').value = \'2024-01-01 18:00\';")\n'
        '    page.fill("{form_description}", "这是一个测试活动")\n'
        '    page.click(\'input[name="locationType"][value="online"]\')\n'
        f'    page.fill("{form_online_platform}", "{online_platform}")\n'
        '    page.click("{btn_submit}")\n'
        '    page.wait_for_selector("{confirm_modal}", state="visible")\n'
        '    page.click("{btn_confirm}")\n'
        "    self.wait_for_toast(page)\n"
        '    expect(page.locator("{toast}")).to_contain_text("{success_create}")\n'
        "```\n"
    ).format(**context)


def get_error_example(context: dict) -> str:
    # 从 context 获取示例数据
    example_data = context.get('example_data', {})
    activity_type = example_data.get('activity_type', '社区活动')
    sub_type = example_data.get('sub_type', '运动会')
    online_platform = example_data.get('online_platform', '腾讯会议')
    
    return (
        "\n## 示例：测试活动名称为空\n"
        "```python\n"
        '@allure.feature("{feature_name}")\n'
        '@allure.title("{tc_id}: 测试活动名称为空")\n'
        "def {method_name}(self, page):\n"
        "    self.navigate_to_page(page)\n"
        '    page.click("{btn_create}")\n'
        '    page.wait_for_selector("{create_modal}", state="visible")\n'
        "    # 活动名称留空\n"
        f'    page.select_option("{form_type}", "{activity_type}")\n'
        '    page.wait_for_selector("#subTypeDiv", state="visible")\n'
        f'    page.select_option("{form_sub_type}", "{sub_type}")\n'
        '    page.evaluate("document.querySelector(\'{form_start_time}\').value = \'2024-01-01 10:00\';")\n'
        '    page.evaluate("document.querySelector(\'{form_end_time}\').value = \'2024-01-01 18:00\';")\n'
        '    page.fill("{form_description}", "这是一个测试活动")\n'
        '    page.click(\'input[name="locationType"][value="online"]\')\n'
        f'    page.fill("{form_online_platform}", "{online_platform}")\n'
        '    page.click("{btn_submit}")\n'
        "    # 验证错误 toast（不要等待确认弹框）\n"
        '    expect(page.locator("{toast}")).to_contain_text("{error_empty_name}")\n'
        '    expect(page.locator("#error_formName")).to_be_visible()\n'
        "```\n"
    ).format(**context)


# ==================== Prompt 组装函数 ====================
def build_test_method_prompt(context: dict) -> str:
    """组装测试方法生成 Prompt"""
    
    # 基础信息
    prompt_parts = [
        "请为以下测试点生成一个 pytest 测试方法。",
        "",
        f"测试点：{context.get('tc_desc', '')}",
        f"模块：{context.get('module_name', '')}",
        f"功能：{context.get('feature_name', '')}",
        f'BASE_URL = "{context.get("base_url", "http://localhost:8080")}"',
        "",
        "## 方法名必须使用（不能自己编造）：",
        f"方法名 = {context.get('method_name', '')}",
        "",
        "请严格按照以下格式输出：",
        f'    @allure.feature("{context.get("feature_name", "")}")',
        f'    @allure.title("{context.get("tc_id", "")}: {context.get("safe_title", "")}")',
        f"    def {context.get('method_name', '')}(self, page):",
        "        # 测试步骤",
        "        pass",
    ]
    
    # 添加片段
    fragments = context.get('fragments', ['base_flow', 'date_picker', 'assertion', 'output_format'])
    
    if 'base_flow' in fragments:
        prompt_parts.append(get_base_flow(context))
    
    if 'date_picker' in fragments:
        prompt_parts.append(get_date_picker_hint(context))
    
    if 'assertion' in fragments:
        prompt_parts.append(get_assertion_hint(context))
    
    if 'output_format' in fragments:
        prompt_parts.append(OUTPUT_FORMAT)
    
    if 'sub_type' in fragments:
        prompt_parts.append(get_sub_type_rule(context))
    
    if 'toast' in fragments:
        prompt_parts.append(TOAST_HINT)
    
    if 'error_elements' in fragments:
        prompt_parts.append(ERROR_ELEMENTS)
    
    if 'cascade' in fragments:
        prompt_parts.append(get_cascade_rule(context))
    
    if 'confirm_modal' in fragments:
        prompt_parts.append(get_confirm_modal_rule(context))
    
    if 'draft' in fragments:
        prompt_parts.append(get_draft_hint(context))
    
    if 'submit' in fragments:
        prompt_parts.append(get_submit_hint(context))
    
    if 'key_points' in fragments:
        prompt_parts.append(KEY_POINTS)
    
    if 'success_example' in fragments:
        prompt_parts.append(get_success_example(context))
    
    if 'error_example' in fragments:
        prompt_parts.append(get_error_example(context))
    
    prompt_parts.append("\n请直接输出测试方法代码：")
    
    return '\n'.join(prompt_parts)