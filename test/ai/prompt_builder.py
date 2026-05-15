# test/ai/prompt_builder.py
"""Prompt 构建器 - 将长 prompt 拆解为可复用片段"""


class PromptBuilder:
    """Prompt 构建器"""
    
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