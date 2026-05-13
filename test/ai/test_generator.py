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

try:
    from test.ai.prompts import build_project_context, get_test_categories, TEST_POINTS_PROMPT
    from test.ai.config import get_config, get_generation_config
except ImportError:
    from .prompts import build_project_context, get_test_categories, TEST_POINTS_PROMPT
    from .config import get_config, get_generation_config


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
        # TODO: 实现具体的解析逻辑
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
        """修复缩进 - 区分装饰器、方法定义和方法体"""
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
            
            # 类定义
            if stripped.startswith('class '):
                in_class = True
                in_method = False
                fixed.append(line)
                continue
            
            # 装饰器或方法定义
            if in_class and (stripped.startswith('@') or stripped.startswith('def ')):
                in_method = True
                fixed.append('    ' + stripped)
                continue
            
            # 方法体
            if in_method:
                # 检测 for 循环
                if stripped.startswith('for '):
                    in_for_loop = True
                    fixed.append('        ' + stripped)
                elif in_for_loop:
                    # for 循环内的代码，12空格
                    fixed.append('            ' + stripped)
                    # 检测 for 循环结束
                    if not stripped or stripped.startswith('@') or stripped.startswith('def '):
                        in_for_loop = False
                else:
                    # 普通方法体代码，8空格
                    fixed.append('        ' + stripped)
                
                # 检测方法结束
                if stripped == 'pass' or (stripped and not stripped.startswith(' ') and not stripped.startswith('#')):
                    in_method = False
                    in_for_loop = False
            else:
                fixed.append(line)
        
        return '\n'.join(fixed)

    
    def _clean_generated_code(self, code: str) -> str:
        """清理生成的代码"""
        # 去除 BOM
        if code.startswith('\ufeff'):
            code = code[1:]
        
        # 移除 markdown 代码块标记
        code = re.sub(r'^```python\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```\s*$', '', code)
        code = code.replace('```python', '').replace('```', '')
        
        # 清理重复的 import
        code = self._clean_imports(code)
        
        # 修复缩进
        code = self._fix_indentation(code)
        
        return code
    
    # ==================== 生成方法 ====================
    
    def _get_selectors_hint(self) -> str:
        """从配置中获取选择器提示"""
        selectors = self.config.get("selectors", {})
        error_messages = self.config.get("error_messages", {})
        success_messages = self.config.get("success_messages", {})
        
        # 构建选择器列表
        selectors_list = []
        for key, value in selectors.items():
            if not key.startswith('_'):
                selectors_list.append(f"- {key}: `{value}`")
        
        # 构建错误消息列表
        errors_list = []
        for key, value in error_messages.items():
            errors_list.append(f"- {key}: `{value}`")
        
        # 构建成功消息列表
        success_list = []
        for key, value in success_messages.items():
            success_list.append(f"- {key}: `{value}`")
        
        hint = f"""
## 📋 页面元素选择器（来自配置文件，必须使用）

{chr(10).join(selectors_list[:30])}

## 📋 错误消息（来自配置文件）

{chr(10).join(errors_list)}

## 📋 成功消息（来自配置文件）

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
## ⚠️ 验证规则（来自配置文件）

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
## ⚠️ 级联选择规则（来自配置文件）

"""
        for rule_name, rule in cascade_rules.items():
            hint += f"- {rule.get('description', rule_name)}: 先选择 `{rule.get('parent')}`，等待 `{rule.get('wait_condition', rule.get('child'))}` 出现，再选择 `{rule.get('child')}`\n"
        
        return hint
    
    def generate_single_test_method(self, point: str, index: int, module_name: str, feature_name: str) -> str:
        """生成单个测试方法"""
        
        # 获取增强提示词
        enhanced_hints = get_all_hints(self.project)
        
        # 获取动态配置提示
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
        
        # 清理描述
        tc_desc_clean = re.sub(r'\s+', ' ', tc_desc).strip()
        if not tc_desc_clean:
            tc_desc_clean = re.sub(r'\s+', ' ', point).strip()
            tc_desc_clean = re.sub(r'^TC_\d+\s*[:：\s]*', '', tc_desc_clean).strip()
            if not tc_desc_clean:
                tc_desc_clean = "untitled_test"
        
        # 定义 safe_title
        safe_title = tc_desc_clean[:100].replace('"', '\\"')
        
        # 生成方法名 - 直接使用 TC 编号，更稳定可靠
        method_name = f"test_{tc_id}"
        print(f"DEBUG: 生成方法名: {method_name}")

        
        # 获取实际的选择器（从 HTML 解析）
        html_selectors_hint = ""
        if self.html_selectors and self.html_selectors.get("ids"):
            html_selectors_hint = f"""
        ## 📋 从 HTML 解析到的实际 ID（优先使用）
        {', '.join(self.html_selectors['ids'][:20])}
        """

        
        # 提取配置中需要的变量
        selectors = self.config.get("selectors", {})
        error_msgs = self.config.get("error_messages", {})
        success_msgs = self.config.get("success_messages", {})
        
        # 提取具体的值
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
        
        # 提取错误消息
        error_empty_name = error_msgs.get('empty_name', '请输入活动名称')
        
        # 提取成功消息
        success_create = success_msgs.get('create_success', '活动创建成功')
        
        # 获取验证规则
        validation_rules = self.config.get("validation_rules", {})
        required_for_submit = validation_rules.get("required_fields_for_submit", [])
        
        # 构建 prompt
        prompt = f"""请为以下测试点生成一个 pytest 测试方法。

测试点：{tc_desc_clean}
模块：{module_name}
功能：{feature_name}
BASE_URL = "{self.config.get('base_url', 'http://localhost:8080')}"

## ⚠️ 方法名必须使用（不能自己编造）：
方法名 = {method_name}

请严格按照以下格式输出：
    @allure.feature("{feature_name}")
    @allure.title("{tc_id}: {safe_title}")
    def {method_name}(self, page):
        # 测试步骤
        pass

## 页面操作流程（必须遵守）
1. self.navigate_to_page(page)
2. page.click("{btn_create}")
3. page.wait_for_selector("{create_modal}", state="visible")
4. 填写表单
5. page.click("{btn_submit}") 或 page.click("{btn_save_draft}")

{html_selectors_hint}

{selectors_hint}

{validation_hint}

{cascade_rules_hint}

{enhanced_hints}

## 日期选择器处理
{form_start_time} 和 {form_end_time} 是只读的，必须用 JavaScript：
    page.evaluate("document.querySelector('{form_start_time}').value = '2024-01-01 10:00';")
    page.evaluate("document.querySelector('{form_end_time}').value = '2024-01-01 18:00';")

## 断言语法
    expect(page.locator("{toast}")).to_contain_text("成功")
    expect(page.locator("{toast}")).to_be_visible()

## 输出格式要求
- 不要使用 async def
- 不要使用 @pytest.mark.asyncio
- 不要使用 @allure.it，使用 @allure.title
- 只输出方法代码

## ⚠️ 重要：表单字段的可见性规则

### 子类型下拉框
- 默认不可见
- **必须先选择活动类型** (`{form_type}`) 才会显示
- 示例：
```python
page.select_option("{form_type}", "社区活动")
page.wait_for_selector("#subTypeDiv", state="visible")
page.select_option("{form_sub_type}", "运动会")

### Toast 消息说明
- ✅ 操作成功时：会显示 toast 消息
- ✅ 表单验证失败时：也会显示 toast 消息，同时显示内联错误提示

# 常见错误提示元素
- 活动名称错误：`#error_formName`
- 活动类型错误：`#error_formType`
- 开始时间错误：`#error_formStartTime`
- 结束时间错误：`#error_formEndTime`
- 时间范围错误：`#error_errorTimeRange`

### 验证失败时的处理
- 验证失败会显示 toast 消息
- 同时会显示内联错误提示元素

## ⚠️ 省市区级联规则
- 必须先选择省份，城市的选项才会加载
- 必须先选择城市，区县的选项才会加载
- 示例：
page.select_option("{form_province}", "广东省")
page.wait_for_selector("{form_city} option[value!='']", state="visible")
page.select_option("{form_city}", "深圳市")
page.wait_for_selector("{form_district} option[value!='']", state="visible")
page.select_option("{form_district}", "南山区")

## 确认弹框显示条件

- 只有所有必填字段都填写完整且验证通过时，才会弹出确认弹框
- 表单有错误时不会弹出确认弹框
- 因此，在测试表单验证失败的场景时，**不要等待确认弹框**
- 只有在测试正向成功流程时，才需要等待确认弹框

正向成功流程示例：
# 等待确认弹框
page.wait_for_selector("{confirm_modal}", state="visible")
page.click("{btn_confirm}")
self.wait_for_toast(page)
expect(page.locator("{toast}")).to_contain_text("{success_create}")

## ⚠️ 活动保存草稿说明
- 点击【保存草稿】按钮 (`{btn_save_draft}`) 时：
  - 只验证必填字段（活动名称、活动类型）
  - **不会验证**活动时间、活动简介等非必填字段
  - 保存后状态为"活动待提交"
  - 不会弹出确认弹框

## ⚠️ 活动提交完成创建说明
- 点击【完成创建】按钮 (`{btn_submit}`) 时：
  - 验证所有必填字段（{', '.join(required_for_submit)}）
  - 验证通过后弹出确认弹框 `{confirm_modal}`
  - 点击确认后创建成功，显示 toast `{success_create}`

## 关键要点总结（再次强调）
1. 子类型字段：必须先选活动类型，等待 `#subTypeDiv` 可见
2. 省市区级联：必须按顺序选择，并等待下一级选项加载
3. 文件上传：使用 `page.set_input_files("input[type='file']", "test.pdf")`
4. 错误消息：检查具体字段错误（如 `{error_empty_name}`），不是通用消息
5. 确认弹框：只在正向成功流程中等待
6. 保存草稿：只验证活动名称和活动类型

## 示例：测试活动名称为空
@allure.feature("{feature_name}")
@allure.title("{tc_id}: 测试活动名称为空")
def test_{tc_id}_activity_name_empty(self, page):
    self.navigate_to_page(page)
    page.click("{btn_create}")
    page.wait_for_selector("{create_modal}", state="visible")
    # 活动名称留空
    page.select_option("{form_type}", "社区活动")
    page.wait_for_selector("#subTypeDiv", state="visible")
    page.select_option("{form_sub_type}", "运动会")
    page.evaluate("document.querySelector('{form_start_time}').value = '2024-01-01 10:00';")
    page.evaluate("document.querySelector('{form_end_time}').value = '2024-01-01 18:00';")
    page.fill("{form_description}", "这是一个测试活动")
    page.click('input[name="locationType"][value="online"]')
    page.fill("{form_online_platform}", "腾讯会议")
    # 提交
    page.click("{btn_submit}")
    # 验证错误消息
    expect(page.locator("{toast}")).to_contain_text("{error_empty_name}")
    expect(page.locator("#error_formName")).to_be_visible()

## 示例：测试创建活动成功
@allure.feature("{feature_name}")
@allure.title("{tc_id}: 测试创建活动成功")
def test_{tc_id}_create_activity_success(self, page):
    self.navigate_to_page(page)
    page.click("{btn_create}")
    page.wait_for_selector("{create_modal}", state="visible")
    page.fill("{form_name}", "测试活动")
    page.select_option("{form_type}", "社区活动")
    page.wait_for_selector("#subTypeDiv", state="visible")
    page.select_option("{form_sub_type}", "运动会")
    page.evaluate("document.querySelector('{form_start_time}').value = '2024-01-01 10:00';")
    page.evaluate("document.querySelector('{form_end_time}').value = '2024-01-01 18:00';")
    page.fill("{form_description}", "这是一个测试活动")
    page.click('input[name="locationType"][value="online"]')
    page.fill("{form_online_platform}", "腾讯会议")
    page.set_input_files("input[type='file']", "test.pdf")
    page.click("{btn_submit}")
    page.wait_for_selector("{confirm_modal}", state="visible")
    page.click("{btn_confirm}")
    self.wait_for_toast(page)
    expect(page.locator("{toast}")).to_contain_text("{success_create}")

请直接输出测试方法代码："""

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
            
            # 清理常见的错误格式
            code = code.replace('@pytest.mark.asyncio', '')
            code = code.replace('async def', 'def')
            code = code.replace('@allure.it', '@allure.title')
            code = code.replace('name_fill', 'page.fill')
            code = code.replace('page.wait_for_selector("#formsubType"', 'page.wait_for_selector("#formSubType"')
            
            # 修复断言语法
            code = self._fix_assertion_syntax(code)
            # 修复常见选择器错误
            code = self._fix_selectors(code)
            
            # 确保方法有正确的缩进
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
        """修复选择器中的常见问题"""
        fixed = code
        
        # 1. 修复双井号 ## -> #
        fixed = re.sub(r'##([a-zA-Z#])', r'#\1', fixed)
        fixed = fixed.replace('##', '#')
        
        # 2. 修复 .# 问题
        fixed = fixed.replace('.#', '#')
        
        # 3. 修复错误的按钮ID
        fixed = fixed.replace('#btnDiscard', '#btnCancel')
        fixed = fixed.replace('#btnConfirmDiscard', '#btnConfirmCancel')
        
        # 4. 修复错误的输入框ID
        fixed = fixed.replace('#formTypeDescription', '#formOtherType')
        
        # 5. 修复多出来的 s 问题
        fixed = fixed.replace('#formsSubType', '#formSubType')
        fixed = fixed.replace('#formsDescription', '#formDescription')
        fixed = fixed.replace('#formsName', '#formName')
        fixed = fixed.replace('#formsType', '#formType')
        
        # 6. 删除不存在的方法调用
        fixed = re.sub(r'page\.execute_operation\([^)]+\);?\s*\n?', '', fixed)
        
        # 7. 修复错误的 toast 选择器
        fixed = fixed.replace('.toast-message', '#toast')
        fixed = fixed.replace('.toast', '#toast')
        
        # 8. 修复 page.wait_for_selector 中的错误
        fixed = fixed.replace('page.wait_for_selector(".#toast-message, .#toast"', 'page.wait_for_selector("#toast"')
        
        # 9. 修复二级下拉框的等待（大小写问题）
        fixed = fixed.replace('#formSubtype', '#formSubType')
        fixed = fixed.replace('#formsubType', '#formSubType')

        # 10. 修复错误的文件上传选择器
        fixed = fixed.replace('#formAttachment', '#fileInput')
        
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
    
        return methods  # ✅ 移到循环外面

    def _sanitize_method_name(self, text: str, max_len: int = 40) -> str:
        """将文本转换为合法的方法名"""
        # 移除常见的无关词（避免生成 test_TC_002_toast 这样奇怪的方法名）
        text = re.sub(r'toast|错误|验证|测试|提示|检查|确认', '', text, flags=re.IGNORECASE)
        # 只保留字母、数字、下划线，其他替换为下划线
        name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '_', text)
        # 移除中文字符（方法名最好用英文或数字）
        name = re.sub(r'[\u4e00-\u9fff]+', '', name)
        # 去除首尾下划线
        name = name.strip('_')
        # 转小写
        name = name.lower()
        # 限制长度
        if len(name) > max_len:
            name = name[:max_len]
        # 如果为空，返回默认值
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
        """提取P0测试点"""
        return self._extract_points_by_priority(test_points, "P0")

    def _extract_p1_points(self, test_points: str) -> List[str]:
        """提取P1测试点"""
        return self._extract_points_by_priority(test_points, "P1")

    def _extract_p2_points(self, test_points: str) -> List[str]:
        """提取P2测试点"""
        return self._extract_points_by_priority(test_points, "P2")

    def _extract_points_by_priority(self, test_points: str, priority: str) -> List[str]:
        """按优先级提取测试点"""
        points = []
        lines = test_points.split('\n')
        in_target = False
        
        for line in lines:
            if f"## {priority}" in line or f"### {priority}" in line:
                in_target = True
            elif in_target and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                points.append(line.strip())
            elif in_target and line.strip() and not line.startswith(('#', '`')):
                # 退出条件
                if any(p in line for p in ['## P', '### P']):
                    in_target = False
        
        # 如果没有找到带优先级的，提取所有带TC_的行
        if not points:
            for line in lines:
                if 'TC_' in line and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                    points.append(line.strip())
        
        return points

    def _fix_assertion_syntax(self, code: str) -> str:
        """修复断言语法"""
        fixed = code
        
        # 修复 to_have_count -> count() 断言
        def replace_to_have_count(match):
            locator = match.group(1)
            expected = match.group(2)
            return f'assert {locator}.count() == {expected}'
        
        fixed = re.sub(
            r'expect\((.*?)\)\.to_have_count\((\d+)\)',
            replace_to_have_count,
            fixed
        )
        
        # 修复 to_have_count 的其他形式
        fixed = re.sub(
            r'\.to_have_count\((\d+)\)',
            lambda m: f'.count() == {m.group(1)}',
            fixed
        )
        
        return fixed

    def generate_in_batches(self, requirement: str, module_name: str, feature_name: str, batch_size: int = 5) -> Dict[str, Any]:
        """逐个生成测试用例（避免截断）"""
        print(f"\n📋 步骤1：分析需求...")
        
        if os.path.isfile(requirement):
            with open(requirement, 'r', encoding='utf-8') as f:
                requirement_content = f.read()
            print(f"  需求长度: {len(requirement_content)} 字符")
        else:
            requirement_content = requirement
            print(f"  需求长度: {len(requirement_content)} 字符")
        
        print(f"\n📝 步骤2：生成测试点...")
        test_points = self.generate_test_points(requirement_content, module_name, feature_name)
        
        if not test_points:
            print(f"  ❌ 未生成测试点")
            return {"test_points": "", "test_data": "", "test_code": ""}
        
        print(f"\n📊 步骤3：解析测试点...")
        p0_points = self._extract_p0_points(test_points)
        p1_points = self._extract_p1_points(test_points)
        p2_points = self._extract_p2_points(test_points)
        
        all_points = p0_points + p1_points + p2_points

        # 去重（基于 TC_xxx 编号）
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
        
        # 【新增】重新编号，确保连续
        if self.gen_config.get("renumber_tests", True):
            print("    🔄 重新编号测试点以确保连续性...")
            all_points = self._renumber_test_points(all_points)
        
        print(f"\n  📊 统计: 共 {len(all_points)} 个测试点")
        print(f"    P0: {len(p0_points)} 个, P1: {len(p1_points)} 个, P2: {len(p2_points)} 个")
        
        print(f"\n🔧 步骤4：逐个生成测试方法（避免截断）...")
        print(f"  共 {len(all_points)} 个测试点，将逐个生成...")
        
        # 逐个生成测试方法
        test_methods = self.generate_all_methods(all_points, module_name, feature_name)
        
        # 构建最终代码 - 使用列表确保正确的缩进和主函数位置
        base_url = self.config.get('base_url', 'http://localhost:8080')
        
        # 构建选择器注释（如果从 HTML 解析到了）
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
            '            page.wait_for_selector(".toast-message, .toast", timeout=timeout)',
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
        
        # 添加所有测试方法
        for method in test_methods:
            if method.strip():
                method_lines = method.split('\n')
                for ml in method_lines:
                    if ml.strip():
                        stripped = ml.lstrip()
                        # 关键：区分装饰器/方法定义 和 方法体
                        if stripped.startswith('def ') or stripped.startswith('@allure'):
                            code_lines.append('    ' + stripped)      # 4空格
                        else:
                            code_lines.append('        ' + stripped)  # 8空格
                    else:
                        code_lines.append('')
                code_lines.append('')

        
        # 修复：主函数必须放在类外部（无缩进）
        code_lines.append('')
        code_lines.append('')
        code_lines.append('if __name__ == "__main__":')
        code_lines.append('    pytest.main([__file__, "-v", "--tb=short"])')
        code_lines.append('')
        
        final_code = '\n'.join(code_lines)
        
        # 最后一次清理：确保断言语法正确
        final_code = self._fix_assertion_syntax(final_code)
        
        # 构建测试点摘要
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
        """保存生成的文件，支持需求标识"""
        if not result.get("test_code"):
            print("⚠️ 没有生成任何测试代码，跳过保存")
            return
        
        project_name = self.config.get("project_name", self.project).replace(" ", "_")
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        # 生成需求标识
        if requirement_info:
            if os.path.isfile(requirement_info):
                req_name = os.path.splitext(os.path.basename(requirement_info))[0]
                req_name = re.sub(r'[^\w\-_]', '_', req_name)
            else:
                req_name = re.sub(r'[^\w\-_]', '_', requirement_info[:30].strip())
        else:
            req_name = None
        
        # 保存测试点
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
        
        # 保存测试代码
        test_code = result.get("test_code", "")
        if test_code:
            test_code = self._clean_generated_code(test_code)
            test_code = self._ensure_main_block_outside_class(test_code)
            
            # 修复：metadata 字符串不要有任何前导空格，且末尾不要有多余换行
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
            
            # 修复 import 前的缩进（如果有）
            test_code = re.sub(r'\n    (import pytest)', r'\n\1', test_code)
            
            # 生成文件名
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
        
        # 查找主函数位置
        main_start = -1
        main_end = -1
        for i, line in enumerate(lines):
            if 'if __name__ == "__main__"' in line:
                main_start = i
                # 找到主函数块的结束
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(('    ', '\t')):
                        main_end = j
                        break
                if main_end == -1:
                    main_end = len(lines)
                break
        
        # 如果主函数不存在，在文件末尾添加正确格式
        if main_start == -1:
            code = code.rstrip() + '\n\n\nif __name__ == "__main__":\n    pytest.main([__file__, "-v", "--tb=short"])\n'
            return code
        
        # 提取主函数块，并修正格式
        main_block_lines = []
        for i in range(main_start, main_end):
            line = lines[i]
            stripped = line.strip()
            if i == main_start:
                # 主函数行
                main_block_lines.append('if __name__ == "__main__":')
            elif stripped:
                # 主函数体内的代码，确保有4个空格缩进
                main_block_lines.append('    ' + stripped)
            else:
                main_block_lines.append('')
        
        # 移除原位置的主函数及其后的空行
        new_lines = lines[:main_start]
        # 跳过主函数块
        i = main_end
        while i < len(lines) and not lines[i].strip():
            i += 1
        new_lines.extend(lines[i:])
        
        # 找到类结束的位置（最后一个类定义结束）
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
        
        # 在类结束后插入主函数
        if class_end != -1:
            insert_pos = class_end
        else:
            insert_pos = len(new_lines)
        
        # 确保有空行分隔
        while insert_pos > 0 and insert_pos < len(new_lines) and not new_lines[insert_pos - 1].strip():
            insert_pos -= 1
        
        # 添加空行
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
        
        # 最终清理：确保主函数格式正确
        # 修复可能出现的 "if __name__ == "__main__":\n\npytest.main" 格式
        result = re.sub(
            r'if __name__ == "__main__":\s*\n\s*pytest\.main',
            'if __name__ == "__main__":\n    pytest.main',
            result
        )
        # 修复可能缺少的缩进
        result = re.sub(
            r'if __name__ == "__main__":\n([^ ])',
            'if __name__ == "__main__":\n    \1',
            result
        )
        
        return result

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def run_and_save(self, requirement: str, module_name: str, feature_name: str, 
                    use_batch: bool = True, batch_size: int = 5, req_identifier: str = None):
        """运行生成器并保存结果，支持需求标识"""
        # 如果没有指定需求标识，从 requirement 参数提取
        if req_identifier is None:
            req_identifier = requirement
        
        result = self.generate_in_batches(requirement, module_name, feature_name, batch_size)
        self.save_to_file(result, requirement_info=req_identifier)
        return result

    def _renumber_test_points(self, points: List[str]) -> List[str]:
        """重新编号测试点，使其连续"""
        renamed_points = []
        for i, point in enumerate(points, 1):
            # 查找原有的 TC_XXX
            new_tc_id = f"TC_{i:03d}"
            # 替换原有的 TC 编号
            new_point = re.sub(r'TC_\d+', new_tc_id, point, count=1)
            renamed_points.append(new_point)
        return renamed_points

def get_generator(project: str = "juice"):
    """获取生成器实例"""
    return AITestGenerator(project=project)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 测试用例生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述或文件路径")
    parser.add_argument("-m", "--module", required=True, help="模块名称")
    parser.add_argument("-f", "--feature", required=True, help="功能名称")
    parser.add_argument("--project", default="juice", help="项目名称")
    parser.add_argument("-o", "--output-name", default=None, help="输出文件名标识（用于区分不同需求）")
    
    args = parser.parse_args()
    
    generator = AITestGenerator(project=args.project)
    
    # 确定输出标识
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
        print(result["test_points"][:1000])# ... 其余方法保持不变 ...