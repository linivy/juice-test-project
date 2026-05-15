# test/ai/test_generator.py
"""AI 测试用例生成器 - 完整优化版"""

import os
import re
import sys
from typing import Optional, Dict, Any, List, Tuple
from test.ai.config import get_config, get_generation_config, get_all_hints

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("请安装 openai: pip install openai")


# ==================== Prompt 构建器 ====================
class PromptBuilder:
    """Prompt 构建器 - 将长 prompt 拆解为可复用片段"""
    
    @staticmethod
    def build_base_info(context: dict) -> list:
        """构建基础信息部分"""
        return [
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
    
    @staticmethod
    def build_base_flow(context: dict) -> str:
        """构建基础操作流程"""
        return (
            "\n## 页面操作流程（必须遵守）\n"
            "1. self.navigate_to_page(page)\n"
            '2. page.click("{btn_create}")\n'
            '3. page.wait_for_selector("{create_modal}", state="visible")\n'
            "4. 填写表单\n"
            '5. page.click("{btn_submit}") 或 page.click("{btn_save_draft}")\n'
        ).format(**context)
    
    @staticmethod
    def build_date_picker_hint(context: dict) -> str:
        """构建日期选择器提示"""
        return (
            "\n## 日期选择器处理\n"
            "{form_start_time} 和 {form_end_time} 是只读的，必须用 JavaScript：\n"
            "    page.evaluate(\"document.querySelector('{form_start_time}').value = '2024-01-01 10:00';\")\n"
            "    page.evaluate(\"document.querySelector('{form_end_time}').value = '2024-01-01 18:00';\")\n"
        ).format(**context)
    
    @staticmethod
    def build_assertion_hint(context: dict) -> str:
        """构建断言语法提示"""
        return (
            "\n## 断言语法\n"
            '    expect(page.locator("{toast}")).to_contain_text("成功")\n'
            '    expect(page.locator("{toast}")).to_be_visible()\n'
        ).format(**context)
    
    @staticmethod
    def build_output_format() -> str:
        """构建输出格式要求"""
        return (
            "\n## 输出格式要求\n"
            "- 不要使用 async def\n"
            "- 不要使用 @pytest.mark.asyncio\n"
            "- 不要使用 @allure.it，使用 @allure.title\n"
            "- 只输出方法代码\n"
        )
    
    @staticmethod
    def build_sub_type_rule(context: dict) -> str:
        """构建子类型下拉框规则"""
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
    
    @staticmethod
    def build_toast_hint() -> str:
        """构建 Toast 消息说明"""
        return (
            "\n### Toast 消息说明\n"
            "- ✅ 操作成功时：会显示 toast 消息\n"
            "- ✅ 表单验证失败时：也会显示 toast 消息，同时显示内联错误提示\n"
        )
    
    @staticmethod
    def build_error_elements() -> str:
        """构建错误提示元素"""
        return (
            "\n### 常见错误提示元素\n"
            "- 活动名称错误：`#error_formName`\n"
            "- 活动类型错误：`#error_formType`\n"
            "- 开始时间错误：`#error_formStartTime`\n"
            "- 结束时间错误：`#error_formEndTime`\n"
            "- 时间范围错误：`#error_errorTimeRange`\n"
        )
    
    @staticmethod
    def build_cascade_rule(context: dict) -> str:
        """构建省市区级联规则"""
        return (
            "\n## 省市区级联规则\n"
            "- 必须先选择省份，城市的选项才会加载\n"
            "- 必须先选择城市，区县的选项才会加载\n"
            "- 示例：\n"
            "```python\n"
            'page.select_option("{form_province}", "广东省")\n'
            'page.wait_for_selector("{form_city} option:not([value=\'\'])", state="visible")\n'
            'page.select_option("{form_city}", "深圳市")\n'
            'page.wait_for_selector("{form_district} option:not([value=\'\'])", state="visible")\n'
            'page.select_option("{form_district}", "南山区")\n'
            "```\n"
        ).format(**context)
    
    @staticmethod
    def build_confirm_modal_rule(context: dict) -> str:
        """构建确认弹框规则"""
        return (
            "\n## 确认弹框显示条件\n"
            "\n"
            "- 只有所有必填字段都填写完整且验证通过时，才会弹出确认弹框\n"
            "- 表单有错误时不会弹出确认弹框\n"
            "- 因此，在测试表单验证失败的场景时，**不要等待确认弹框**\n"
            "- 只有在测试正向成功流程时，才需要等待确认弹框\n"
            "\n"
            "正向成功流程示例：\n"
            "```python\n"
            'page.wait_for_selector("{confirm_modal}", state="visible")\n'
            'page.click("{btn_confirm}")\n'
            "self.wait_for_toast(page)\n"
            'expect(page.locator("{toast}")).to_contain_text("{success_create}")\n'
            "```\n"
        ).format(**context)
    
    @staticmethod
    def build_draft_hint(context: dict) -> str:
        """构建保存草稿说明"""
        return (
            "\n## 活动保存草稿说明\n"
            "- 点击【保存草稿】按钮 (`{btn_save_draft}`) 时：\n"
            "  - 只验证必填字段（活动名称、活动类型）\n"
            "  - **不会验证**活动时间、活动简介等非必填字段\n"
            "  - 保存后状态为\"活动待提交\"\n"
            "  - 不会弹出确认弹框\n"
        ).format(**context)
    
    @staticmethod
    def build_submit_hint(context: dict) -> str:
        """构建提交创建说明"""
        required_fields_str = ', '.join(context.get('required_for_submit', []))
        return (
            "\n## 活动提交完成创建说明\n"
            "- 点击【完成创建】按钮 (`{btn_submit}`) 时：\n"
            f"  - 验证所有必填字段（{required_fields_str}）\n"
            "  - 验证通过后弹出确认弹框 `{confirm_modal}`\n"
            "  - 点击确认后创建成功，显示 toast `{success_create}`\n"
        ).format(**context)
    
    @staticmethod
    def build_key_points() -> str:
        """构建关键要点总结"""
        return (
            "\n## 关键要点总结（再次强调）\n"
            "1. 子类型字段：必须先选活动类型，等待 `#subTypeDiv` 可见\n"
            "2. 省市区级联：必须按顺序选择，并等待下一级选项加载\n"
            "3. 文件上传：使用 `page.set_input_files(\"input[type='file']\", \"test.pdf\")`\n"
            "4. 错误消息：检查具体字段错误，不是通用消息\n"
            "5. 确认弹框：只在正向成功流程中等待\n"
            "6. 保存草稿：只验证活动名称和活动类型\n"
        )
    
    @staticmethod
    def build_success_example(context: dict) -> str:
        """构建成功示例"""
        return (
            "\n## 示例：测试创建活动成功\n"
            "```python\n"
            '@allure.feature("{feature_name}")\n'
            '@allure.title("{tc_id}: 测试创建活动成功")\n'
            "def {method_name}(self, page):\n"
            "    self.navigate_to_page(page)\n"
            '    page.click("{btn_create}")\n'
            '    page.wait_for_selector("{create_modal}", state="visible")\n'
            '    page.fill("{form_name}", "测试活动")\n'
            '    page.select_option("{form_type}", "社区活动")\n'
            '    page.wait_for_selector("#subTypeDiv", state="visible")\n'
            '    page.select_option("{form_sub_type}", "运动会")\n'
            '    page.evaluate("document.querySelector(\'{form_start_time}\').value = \'2024-01-01 10:00\';")\n'
            '    page.evaluate("document.querySelector(\'{form_end_time}\').value = \'2024-01-01 18:00\';")\n'
            '    page.fill("{form_description}", "这是一个测试活动")\n'
            '    page.click(\'input[name="locationType"][value="online"]\')\n'
            '    page.fill("{form_online_platform}", "腾讯会议")\n'
            '    page.click("{btn_submit}")\n'
            '    page.wait_for_selector("{confirm_modal}", state="visible")\n'
            '    page.click("{btn_confirm}")\n'
            "    self.wait_for_toast(page)\n"
            '    expect(page.locator("{toast}")).to_contain_text("{success_create}")\n'
            "```\n"
        ).format(**context)
    
    @staticmethod
    def build_error_example(context: dict) -> str:
        """构建错误示例"""
        return (
            "\n## 示例：测试活动名称为空\n"
            "```python\n"
            '@allure.feature("{feature_name}")\n'
            '@allure.title("{tc_id}: 测试活动名称为空")\n'
            "def {method_name}(self, page):\n"
            "    self.navigate_to_page(page)\n"
            '    page.click("{btn_create}")\n'
            '    page.wait_for_selector("{create_modal}", state="visible")\n'
            '    page.select_option("{form_type}", "社区活动")\n'
            '    page.wait_for_selector("#subTypeDiv", state="visible")\n'
            '    page.select_option("{form_sub_type}", "运动会")\n'
            '    page.evaluate("document.querySelector(\'{form_start_time}\').value = \'2024-01-01 10:00\';")\n'
            '    page.evaluate("document.querySelector(\'{form_end_time}\').value = \'2024-01-01 18:00\';")\n'
            '    page.fill("{form_description}", "这是一个测试活动")\n'
            '    page.click(\'input[name="locationType"][value="online"]\')\n'
            '    page.fill("{form_online_platform}", "腾讯会议")\n'
            '    page.click("{btn_submit}")\n'
            '    expect(page.locator("{toast}")).to_contain_text("{error_empty_name}")\n'
            '    expect(page.locator("#error_formName")).to_be_visible()\n'
            "```\n"
        ).format(**context)
    
    @classmethod
    def build_prompt(cls, context: dict) -> str:
        """组装完整的 prompt"""
        prompt_parts = cls.build_base_info(context)
        
        # 添加固定片段
        prompt_parts.append(cls.build_base_flow(context))
        prompt_parts.append(cls.build_date_picker_hint(context))
        prompt_parts.append(cls.build_assertion_hint(context))
        prompt_parts.append(cls.build_output_format())
        prompt_parts.append(cls.build_sub_type_rule(context))
        prompt_parts.append(cls.build_toast_hint())
        prompt_parts.append(cls.build_error_elements())
        prompt_parts.append(cls.build_cascade_rule(context))
        prompt_parts.append(cls.build_confirm_modal_rule(context))
        prompt_parts.append(cls.build_draft_hint(context))
        prompt_parts.append(cls.build_submit_hint(context))
        prompt_parts.append(cls.build_key_points())
        prompt_parts.append(cls.build_success_example(context))
        prompt_parts.append(cls.build_error_example(context))
        
        prompt_parts.append("\n请直接输出测试方法代码：")
        
        return '\n'.join(prompt_parts)


# ==================== AI 测试生成器主类 ====================
class AITestGenerator:
    """AI 测试用例生成器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat", project: str = "juice"):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        self.model = model
        self.project = project
        self.config = get_config(project)
        self.gen_config = get_generation_config(project)
        self.html_selectors = self._parse_html_selectors() if project == "activity" else {}
    
    # ==================== 辅助方法 ====================
    
    def _parse_html_selectors(self) -> Dict[str, Any]:
        """解析 HTML 获取所有可用的 ID/选择器"""
        return {"ids": [], "classes": []}
    
    def _clean_imports(self, code: str) -> str:
        """清理重复的 import"""
        lines = code.split('\n')
        seen_imports = set()
        cleaned = []
        for line in lines:
            if line.startswith('import ') or line.startswith('from '):
                if line not in seen_imports:
                    seen_imports.add(line)
                    cleaned.append(line)
            else:
                cleaned.append(line)
        return '\n'.join(cleaned)
    
    def _fix_indentation(self, code: str) -> str:
        """修复缩进 - 正确处理 for 循环内的代码"""
        lines = code.split('\n')
        fixed = []
        in_class = False
        in_method = False
        in_for_loop = False
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                fixed.append(line)
                continue
            
            if stripped.startswith('class '):
                in_class = True
                in_method = False
                in_for_loop = False
                fixed.append(line)
                continue
            
            if in_class and (stripped.startswith('@') or stripped.startswith('def ')):
                in_method = True
                in_for_loop = False
                if not line.startswith('    '):
                    fixed.append('    ' + line.lstrip())
                else:
                    fixed.append(line)
                continue
            
            if in_method:
                if stripped.startswith('for '):
                    in_for_loop = True
                    if not line.startswith('        '):
                        fixed.append('        ' + line.lstrip())
                    else:
                        fixed.append(line)
                elif in_for_loop:
                    if not line.startswith('            '):
                        fixed.append('            ' + line.lstrip())
                    else:
                        fixed.append(line)
                    if not stripped or stripped.startswith(('@', 'def ', 'class ')):
                        in_for_loop = False
                else:
                    if not line.startswith('        '):
                        fixed.append('        ' + line.lstrip())
                    else:
                        fixed.append(line)
                
                if stripped == 'pass' or (stripped and not stripped.startswith(('@', 'def ', 'for ', 'class ')) and len(stripped) < 3):
                    in_method = False
                    in_for_loop = False
            else:
                fixed.append(line)
        
        return '\n'.join(fixed)
    
    def _clean_generated_code(self, code: str) -> str:
        """清理生成的代码"""
        if not code:
            return code
        
        code = re.sub(r'^```python\s*\n?', '', code, flags=re.MULTILINE)
        code = re.sub(r'```\s*\n?', '', code)
        code = code.replace('```python', '').replace('```', '')
        
        code = re.sub(r'^\s*python\s*\n?', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n\s*python\s*\n', '\n', code)
        
        code = code.replace('[COMPLETE]', '')
        
        code = self._fix_selectors(code)
        code = self._fix_assertion_syntax(code)
        code = self._fix_indentation(code)
        code = self._clean_imports(code)
        code = re.sub(r'\n{3,}', '\n\n', code)
        code = code.rstrip() + '\n'
        
        return code
    
    # ==================== 生成方法 ====================
    
    def _get_selectors_hint(self) -> str:
        """从配置中获取选择器提示"""
        selectors = self.config.get("selectors", {})
        error_messages = self.config.get("error_messages", {})
        success_messages = self.config.get("success_messages", {})
        
        selectors_list = []
        for key, value in selectors.items():
            if not key.startswith('_'):
                selectors_list.append(f"- {key}: `{value}`")
        
        errors_list = []
        for key, value in error_messages.items():
            errors_list.append(f"- {key}: `{value}`")
        
        success_list = []
        for key, value in success_messages.items():
            success_list.append(f"- {key}: `{value}`")
        
        hint = f"""
## 页面元素选择器（来自配置文件，必须使用）

{chr(10).join(selectors_list[:30])}

## 错误消息（来自配置文件）

{chr(10).join(errors_list)}

## 成功消息（来自配置文件）

{chr(10).join(success_list)}
"""
        return hint
    
    def _get_validation_rules_hint(self) -> str:
        """从配置中获取验证规则提示"""
        validation_rules = self.config.get("validation_rules", {})
        required_for_submit = validation_rules.get("required_fields_for_submit", [])
        required_for_draft = validation_rules.get("required_fields_for_draft", [])
        field_limits = validation_rules.get("field_limits", {})
        
        hint = f"""
## 验证规则（来自配置文件）

### 提交时必填字段
{', '.join([f'`{f}`' for f in required_for_submit])}

### 保存草稿时必填字段
{', '.join([f'`{f}`' for f in required_for_draft])}

### 字段长度限制
"""
        for field, limit in field_limits.items():
            hint += f"- `{field}`: 最多 {limit} 字符\n"
        
        return hint
    
    def _get_cascade_rules_hint(self) -> str:
        """从配置中获取级联规则提示"""
        cascade_rules = self.config.get("cascade_rules", {})
        
        if not cascade_rules:
            return ""
        
        hint = """
## 级联选择规则（来自配置文件）

"""
        for rule_name, rule in cascade_rules.items():
            hint += f"- {rule.get('description', rule_name)}: 先选择 `{rule.get('parent')}`，等待 `{rule.get('wait_condition', rule.get('child'))}` 出现，再选择 `{rule.get('child')}`\n"
        
        return hint
    
    def generate_single_test_method(self, point: str, index: int, module_name: str, feature_name: str) -> str:
        """生成单个测试方法"""
        
        enhanced_hints = get_all_hints(self.project)
        selectors_hint = self._get_selectors_hint()
        validation_hint = self._get_validation_rules_hint()
        cascade_rules_hint = self._get_cascade_rules_hint()
        
        # 提取 TC 编号和描述
        tc_pattern = r'^(?:[-*•]\s*)?(TC_\d+)\s*[:：\s]\s*(.*)'
        match = re.match(tc_pattern, point, re.DOTALL)
        
        if match:
            tc_id = match.group(1)
            tc_desc = match.group(2).strip()
        else:
            tc_match = re.search(r'(TC_\d+)', point)
            if tc_match:
                tc_id = tc_match.group(1)
                tc_desc = re.sub(r'^.*?TC_\d+\s*[:：\s]*', '', point).strip()
            else:
                tc_id = f"TC_{index:03d}"
                tc_desc = point.strip()
        
        tc_desc_clean = re.sub(r'\s+', ' ', tc_desc).strip()
        if not tc_desc_clean:
            tc_desc_clean = re.sub(r'\s+', ' ', point).strip()
            tc_desc_clean = re.sub(r'^TC_\d+\s*[:：\s]*', '', tc_desc_clean).strip()
            if not tc_desc_clean:
                tc_desc_clean = "untitled_test"
        
        safe_title = tc_desc_clean[:100].replace('"', '\\"')
        method_name = f"test_{tc_id}"
        print(f"DEBUG: 生成方法名: {method_name}")
        
        html_selectors_hint = ""
        if self.html_selectors and self.html_selectors.get("ids"):
            html_selectors_hint = f"""
## 从 HTML 解析到的实际 ID（优先使用）
{', '.join(self.html_selectors['ids'][:20])}
"""
        
        selectors = self.config.get("selectors", {})
        error_msgs = self.config.get("error_messages", {})
        success_msgs = self.config.get("success_messages", {})
        
        btn_create = selectors.get('btn_create', '#btnCreate')
        btn_submit = selectors.get('btn_submit', '#btnSubmit')
        btn_save_draft = selectors.get('btn_save_draft', '#btnSaveDraft')
        btn_confirm = selectors.get('btn_confirm', '#btnConfirm')
        create_modal = selectors.get('create_modal', '#createModal')
        confirm_modal = selectors.get('confirm_modal', '#confirmModal')
        form_name = selectors.get('form_name', '#formName')
        form_type = selectors.get('form_type', '#formType')
        form_sub_type = selectors.get('form_sub_type', '#formSubType')
        form_start_time = selectors.get('form_start_time', '#formStartTime')
        form_end_time = selectors.get('form_end_time', '#formEndTime')
        form_description = selectors.get('form_description', '#formDescription')
        form_online_platform = selectors.get('form_online_platform', '#formOnlinePlatform')
        form_province = selectors.get('form_province', '#formProvince')
        form_city = selectors.get('form_city', '#formCity')
        form_district = selectors.get('form_district', '#formDistrict')
        toast = selectors.get('toast', '#toast')
        
        error_empty_name = error_msgs.get('empty_name', '请输入活动名称')
        success_create = success_msgs.get('create_success', '活动创建成功')
        
        validation_rules = self.config.get("validation_rules", {})
        required_for_submit = validation_rules.get("required_fields_for_submit", [])

        # 获取配置中的额外数据
        example_data = self.config.get('example_data', {})
        field_labels = self.config.get('field_labels', {})
        
        # 构建 context 字典
        context = {
            'tc_desc': tc_desc_clean,
            'tc_id': tc_id,
            'safe_title': safe_title,
            'method_name': method_name,
            'module_name': module_name,
            'feature_name': feature_name,
            'base_url': self.config.get('base_url', 'http://localhost:8080'),
            'btn_create': btn_create,
            'btn_submit': btn_submit,
            'btn_save_draft': btn_save_draft,
            'btn_confirm': btn_confirm,
            'create_modal': create_modal,
            'confirm_modal': confirm_modal,
            'form_name': form_name,
            'form_type': form_type,
            'form_sub_type': form_sub_type,
            'form_start_time': form_start_time,
            'form_end_time': form_end_time,
            'form_description': form_description,
            'form_online_platform': form_online_platform,
            'form_province': form_province,
            'form_city': form_city,
            'form_district': form_district,
            'toast': toast,
            'error_empty_name': error_empty_name,
            'success_create': success_create,
            'required_for_submit': required_for_submit,
            'error_messages': error_msgs,
            'example_data': example_data,
            'field_labels': field_labels,
            'field_error_configs': [
                ('form_name', 'empty_name', field_labels.get('form_name', '字段')),
                ('form_type', 'empty_type', field_labels.get('form_type', '字段')),
                ('form_start_time', 'empty_start_time', field_labels.get('form_start_time', '字段')),
                ('form_end_time', 'empty_end_time', field_labels.get('form_end_time', '字段')),
                ('form_description', 'empty_description', field_labels.get('form_description', '字段')),
            ],
        }
        
        # 使用 PromptBuilder 构建 prompt
        prompt = PromptBuilder.build_prompt(context)
        
        # 添加动态提示词
        prompt += f"\n\n{html_selectors_hint}\n\n{selectors_hint}\n\n{validation_hint}\n\n{cascade_rules_hint}\n\n{enhanced_hints}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是测试自动化专家。只输出测试方法代码，使用同步 def 不要用 async。使用 @allure.title 不要用 @allure.it。使用 page.fill 不要用 name_fill。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            code = response.choices[0].message.content
            
            code = code.replace('@pytest.mark.asyncio', '')
            code = code.replace('async def', 'def')
            code = code.replace('@allure.it', '@allure.title')
            code = code.replace('name_fill', 'page.fill')
            code = code.replace('page.wait_for_selector("#formsubType"', 'page.wait_for_selector("#formSubType"')
            
            code = self._fix_assertion_syntax(code)
            code = self._fix_selectors(code)
            
            if code.strip() and not code.startswith('    '):
                code = '    ' + code
            
            return code
            
        except Exception as e:
            print(f"    ❌ 生成方法 {index} 失败: {e}")
            return f"""
    @allure.feature("{feature_name}")
    @allure.title("{tc_id}: {safe_title}")
    def {method_name}(self, page):
        self.navigate_to_page(page)
        page.click("{btn_create}")
        page.wait_for_selector("{create_modal}", state="visible")
        # TODO: 实现测试步骤
        pass
"""
    
    def _fix_selectors(self, code: str) -> str:
        """修复选择器中的常见问题 - 配置驱动"""
        fixed = code
        
        # 1. 修复双井号和 .# 问题
        fixed = re.sub(r'##([a-zA-Z#])', r'#\1', fixed)
        fixed = fixed.replace('##', '#')
        fixed = fixed.replace('.#', '#')
        
        # 2. 从配置中获取选择器别名映射
        selector_aliases = self.config.get("selector_aliases", {})
        for old, new in selector_aliases.items():
            fixed = fixed.replace(old, new)
        
        # 3. 删除不存在的方法调用
        fixed = re.sub(r'page\.execute_operation\([^)]+\);?\s*\n?', '', fixed)
        
        # 4. 修复二级下拉框的大小写问题
        fixed = fixed.replace('#formSubtype', '#formSubType')
        fixed = fixed.replace('#formsubType', '#formSubType')
        
        # 5. 修复活动类型的 option value - 将显示文本转换为实际 value
        fixed = fixed.replace('page.select_option("#formType", "社区活动")', 'page.select_option("#formType", "community")')
        fixed = fixed.replace('page.select_option("#formType", "家庭活动")', 'page.select_option("#formType", "family")')
        fixed = fixed.replace('page.select_option("#formType", "其他")', 'page.select_option("#formType", "other")')
        
        # 6. 修复取消弹框按钮选择器
        fixed = fixed.replace('#btnCancelDiscard', '#btnConfirm')
        
        # 7. 修复严格模式问题 - 添加 .nth(1) 到 option 断言
        fixed = re.sub(r'expect\(page\.locator\("([^"]*option[^"]*)"\)\.to_contain_text', r'expect(page.locator("\1").nth(1)).to_contain_text', fixed)
        
        # 8. 修复通用错误消息 - 将"活动信息未完善"替换为具体错误
        fixed = fixed.replace('"活动信息未完善"', '"请输入活动名称"')
        fixed = fixed.replace('"活动信息未完善，请前往完善"', '"请输入活动名称"')
        
        return fixed

    def generate_all_methods(self, all_points: List[str], module_name: str, feature_name: str) -> List[str]:
        methods = []
        total = len(all_points)
        
        for i, point in enumerate(all_points, 1):
            print(f"    生成方法 {i}/{total}: {point[:50]}...")
            method = self.generate_single_test_method(point, i, module_name, feature_name)
            methods.append(method)
            if i % 5 == 0:
                print(f"    进度: {i}/{total}")
        
        return methods
    
    def _sanitize_method_name(self, text: str, max_len: int = 40) -> str:
        """将文本转换为合法的方法名"""
        text = re.sub(r'toast|错误|验证|测试|提示|检查|确认', '', text, flags=re.IGNORECASE)
        name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '_', text)
        name = re.sub(r'[\u4e00-\u9fff]+', '', name)
        name = name.strip('_')
        name = name.lower()
        if len(name) > max_len:
            name = name[:max_len]
        if not name:
            name = "test_case"
        return name
    
    def generate_test_points(self, requirement_content: str, module_name: str, feature_name: str) -> str:
        """生成测试点"""
        prompt = f"""请根据以下需求，生成测试点。

需求：{requirement_content}
模块：{module_name}
功能：{feature_name}

请生成测试点，格式如下：
- TC_001: 测试xxx
- TC_002: 测试xxx

请按P0、P1、P2优先级分类输出。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"生成测试点失败: {e}")
            return ""
    
    def _extract_p0_points(self, test_points: str) -> List[str]:
        return self._extract_points_by_priority(test_points, "P0")
    
    def _extract_p1_points(self, test_points: str) -> List[str]:
        return self._extract_points_by_priority(test_points, "P1")
    
    def _extract_p2_points(self, test_points: str) -> List[str]:
        return self._extract_points_by_priority(test_points, "P2")
    
    def _extract_points_by_priority(self, test_points: str, priority: str) -> List[str]:
        points = []
        lines = test_points.split('\n')
        in_target = False
        
        for line in lines:
            if f"## {priority}" in line or f"### {priority}" in line:
                in_target = True
            elif in_target and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                points.append(line.strip())
            elif in_target and line.strip() and not line.startswith(('#', '`')):
                if any(p in line for p in ['## P', '### P']):
                    in_target = False
        
        if not points:
            for line in lines:
                if 'TC_' in line and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                    points.append(line.strip())
        
        return points
    
    def _fix_assertion_syntax(self, code: str) -> str:
        """修复断言语法"""
        fixed = code
        
        def replace_to_have_count(match):
            locator = match.group(1)
            expected = match.group(2)
            return f'assert {locator}.count() == {expected}'
        
        fixed = re.sub(r'expect\((.*?)\)\.to_have_count\((\d+)\)', replace_to_have_count, fixed)
        fixed = re.sub(r'\.to_have_count\((\d+)\)', lambda m: f'.count() == {m.group(1)}', fixed)
        
        return fixed
    
    def generate_in_batches(self, requirement: str, module_name: str, feature_name: str, batch_size: int = 5) -> Dict[str, Any]:
        """逐个生成测试用例（避免截断）"""
        print(f"\n步骤1：分析需求...")
        
        if os.path.isfile(requirement):
            with open(requirement, 'r', encoding='utf-8') as f:
                requirement_content = f.read()
            print(f"  需求长度: {len(requirement_content)} 字符")
        else:
            requirement_content = requirement
            print(f"  需求长度: {len(requirement_content)} 字符")
        
        print(f"\n步骤2：生成测试点...")
        test_points = self.generate_test_points(requirement_content, module_name, feature_name)
        
        if not test_points:
            print(f"  ❌ 未生成测试点")
            return {"test_points": "", "test_data": "", "test_code": ""}
        
        print(f"\n步骤3：解析测试点...")
        p0_points = self._extract_p0_points(test_points)
        p1_points = self._extract_p1_points(test_points)
        p2_points = self._extract_p2_points(test_points)
        
        all_points = p0_points + p1_points + p2_points
        
        seen_tc = set()
        unique_points = []
        for point in all_points:
            tc_match = re.search(r'TC_\d+', point)
            if tc_match:
                tc_id = tc_match.group()
                if tc_id not in seen_tc:
                    seen_tc.add(tc_id)
                    unique_points.append(point)
            else:
                unique_points.append(point)
        all_points = unique_points
        
        if self.gen_config.get("renumber_tests", True):
            print("    🔄 重新编号测试点以确保连续性...")
            all_points = self._renumber_test_points(all_points)
        
        print(f"\n  📊 统计: 共 {len(all_points)} 个测试点")
        print(f"    P0: {len(p0_points)} 个, P1: {len(p1_points)} 个, P2: {len(p2_points)} 个")
        
        print(f"\n步骤4：逐个生成测试方法...")
        print(f"  共 {len(all_points)} 个测试点，将逐个生成...")
        
        test_methods = self.generate_all_methods(all_points, module_name, feature_name)
        
        base_url = self.config.get('base_url', 'http://localhost:8080')
        
        selectors_comment = ""
        if self.html_selectors and self.html_selectors.get("ids"):
            selectors_comment = f"""
# 可用的页面元素 ID（从 HTML 自动解析）：
# {', '.join(self.html_selectors['ids'][:15])}
"""
        
        code_lines = [
            'import pytest',
            'import allure',
            'from playwright.sync_api import expect',
            '',
            f'BASE_URL = "{base_url}"',
            selectors_comment,
            '',
            f'class Test{module_name.title()}:',
            f'    """{feature_name}功能测试自动生成"""',
            '',
            '    def navigate_to_page(self, page):',
            '        """导航到页面"""',
            '        page.goto(BASE_URL)',
            '        page.wait_for_load_state("networkidle")',
            '',
            '    def wait_for_toast(self, page, timeout=3000):',
            '        """等待toast消息"""',
            '        try:',
            '            page.wait_for_selector("#toast", timeout=timeout)',
            '            page.wait_for_timeout(500)',
            '        except:',
            '            pass',
            '',
            '    def close_dialog(self, page):',
            '        """关闭弹窗"""',
            '        try:',
            '            page.locator(".modal-close, .dialog-close, #btnCloseModal").click(timeout=2000)',
            '        except:',
            '            pass',
            '',
        ]
        
        for method in test_methods:
            if method.strip():
                method_lines = method.split('\n')
                for ml in method_lines:
                    if ml.strip():
                        stripped = ml.lstrip()
                        if stripped.startswith('def ') or stripped.startswith('@allure'):
                            code_lines.append('    ' + stripped)
                        else:
                            code_lines.append('        ' + stripped)
                    else:
                        code_lines.append('')
                code_lines.append('')
        
        code_lines.append('')
        code_lines.append('')
        code_lines.append('if __name__ == "__main__":')
        code_lines.append('    pytest.main([__file__, "-v", "--tb=short"])')
        code_lines.append('')
        
        final_code = '\n'.join(code_lines)
        final_code = self._fix_assertion_syntax(final_code)
        
        test_points_summary = f"## P0 ({len(p0_points)}个)\n" + "\n".join([f"- {p}" for p in p0_points])
        if p1_points:
            test_points_summary += f"\n\n## P1 ({len(p1_points)}个)\n" + "\n".join([f"- {p}" for p in p1_points])
        if p2_points:
            test_points_summary += f"\n\n## P2 ({len(p2_points)}个)\n" + "\n".join([f"- {p}" for p in p2_points])
        
        print(f"\n✅ 完成！共生成 {len(test_methods)} 个测试方法")
        
        return {
            "test_points": test_points_summary,
            "test_data": "",
            "test_code": final_code
        }
    
    def save_to_file(self, result: Dict[str, Any], output_dir: str = "test/ai/generated", requirement_info: str = None):
        """保存生成的文件"""
        if not result.get("test_code"):
            print("⚠️ 没有生成任何测试代码，跳过保存")
            return
        
        project_name = self.config.get("project_name", self.project).replace(" ", "_")
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        if requirement_info:
            if os.path.isfile(requirement_info):
                req_name = os.path.splitext(os.path.basename(requirement_info))[0]
                req_name = re.sub(r'[^\w\-_]', '_', req_name)
            else:
                req_name = re.sub(r'[^\w\-_]', '_', requirement_info[:30].strip())
        else:
            req_name = None
        
        test_points_file = f"{project_dir}/test_points"
        if req_name:
            test_points_file += f"_{req_name}"
        test_points_file += ".md"
        
        if result.get("test_points"):
            with open(test_points_file, "w", encoding="utf-8") as f:
                f.write(f"# 测试点文档\n")
                f.write(f"# 生成时间: {self._get_timestamp()}\n")
                f.write(f"# 需求: {requirement_info if requirement_info else '未指定'}\n")
                f.write(f"# 模块: {self.project}\n")
                f.write(f"\n{result['test_points']}\n")
            print(f"📁 测试点已保存: {test_points_file}")
        
        test_code = result.get("test_code", "")
        if test_code:
            test_code = self._clean_generated_code(test_code)
            test_code = self._ensure_main_block_outside_class(test_code)
            
            metadata = '''# -*- coding: utf-8 -*-
"""
AI 生成的自动化测试用例
================================
生成时间: %s
需求: %s
模块: %s
功能: %s
"""

''' % (
    self._get_timestamp(),
    requirement_info if requirement_info else '未指定',
    self.project,
    self.config.get('project_name', '未知')
)
            
            test_code = metadata + test_code
            test_code = re.sub(r'\n    (import pytest)', r'\n\1', test_code)
            
            test_file = f"{project_dir}/generated_test"
            if req_name:
                test_file += f"_{req_name}"
            test_file += ".py"
            
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_code)
            print(f"📁 测试代码已保存: {test_file}")
            print(f"   代码长度: {len(test_code)} 字符")
    
    def _ensure_main_block_outside_class(self, code: str) -> str:
        """确保主函数在类外部且格式正确"""
        lines = code.split('\n')
        
        main_start = -1
        main_end = -1
        for i, line in enumerate(lines):
            if 'if __name__ == "__main__"' in line:
                main_start = i
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(('    ', '\t')):
                        main_end = j
                        break
                if main_end == -1:
                    main_end = len(lines)
                break
        
        if main_start == -1:
            code = code.rstrip() + '\n\n\nif __name__ == "__main__":\n    pytest.main([__file__, "-v", "--tb=short"])\n'
            return code
        
        main_block_lines = []
        for i in range(main_start, main_end):
            line = lines[i]
            stripped = line.strip()
            if i == main_start:
                main_block_lines.append('if __name__ == "__main__":')
            elif stripped:
                main_block_lines.append('    ' + stripped)
            else:
                main_block_lines.append('')
        
        new_lines = lines[:main_start]
        i = main_end
        while i < len(lines) and not lines[i].strip():
            i += 1
        new_lines.extend(lines[i:])
        
        class_end = -1
        in_class = False
        class_indent = -1
        for i, line in enumerate(new_lines):
            stripped = line.strip()
            if stripped.startswith('class '):
                in_class = True
                class_indent = len(line) - len(line.lstrip())
            elif in_class and stripped and not line.startswith(' ' * (class_indent + 4)):
                class_end = i
                in_class = False
        
        if class_end != -1:
            insert_pos = class_end
        else:
            insert_pos = len(new_lines)
        
        while insert_pos > 0 and insert_pos < len(new_lines) and not new_lines[insert_pos - 1].strip():
            insert_pos -= 1
        
        if insert_pos < len(new_lines):
            new_lines.insert(insert_pos, '')
            insert_pos += 1
        new_lines.insert(insert_pos, '')
        insert_pos += 1
        
        for ml in main_block_lines:
            new_lines.insert(insert_pos, ml)
            insert_pos += 1
        new_lines.insert(insert_pos, '')
        
        result = '\n'.join(new_lines)
        
        result = re.sub(r'if __name__ == "__main__":\s*\n\s*pytest\.main', 'if __name__ == "__main__":\n    pytest.main', result)
        result = re.sub(r'if __name__ == "__main__":\n([^ ])', 'if __name__ == "__main__":\n    \1', result)
        
        return result
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run_and_save(self, requirement: str, module_name: str, feature_name: str, 
                    use_batch: bool = True, batch_size: int = 5, req_identifier: str = None):
        if req_identifier is None:
            req_identifier = requirement
        
        result = self.generate_in_batches(requirement, module_name, feature_name, batch_size)
        self.save_to_file(result, requirement_info=req_identifier)
        return result
    
    def _renumber_test_points(self, points: List[str]) -> List[str]:
        renamed_points = []
        for i, point in enumerate(points, 1):
            new_tc_id = f"TC_{i:03d}"
            new_point = re.sub(r'TC_\d+', new_tc_id, point, count=1)
            renamed_points.append(new_point)
        return renamed_points


def get_generator(project: str = "juice"):
    return AITestGenerator(project=project)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 测试用例生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述或文件路径")
    parser.add_argument("-m", "--module", required=True, help="模块名称")
    parser.add_argument("-f", "--feature", required=True, help="功能名称")
    parser.add_argument("--project", default="juice", help="项目名称")
    parser.add_argument("-o", "--output-name", default=None, help="输出文件名标识")
    
    args = parser.parse_args()
    
    generator = AITestGenerator(project=args.project)
    
    output_name = args.output_name
    if output_name is None and os.path.isfile(args.requirement):
        output_name = args.requirement
    
    result = generator.run_and_save(
        args.requirement, args.module, args.feature,
        use_batch=True,
        batch_size=5,
        req_identifier=output_name
    )
    
    if result.get("test_points"):
        print("\n" + "=" * 60)
        print("📋 测试点预览")
        print("=" * 60)
        print(result["test_points"][:1000])