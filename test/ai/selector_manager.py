# test/ai/selector_manager.py
"""选择器管理器 - 封装所有页面元素操作"""

import os
import tempfile
from typing import Optional, Any, Dict
from playwright.sync_api import Page, expect


class SelectorManager:
    """选择器管理器 - 基础操作"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化选择器管理器
        
        Args:
            config: 配置字典，包含 selectors, error_messages, success_messages
        """
        self.config = config
        self.selectors = config.get('selectors', {})
        self.error_msgs = config.get('error_messages', {})
        self.success_msgs = config.get('success_messages', {})
    
    def get(self, name: str, default: Optional[str] = None) -> str:
        """获取选择器"""
        return self.selectors.get(name, default or f'#{name}')
    
    # ==================== 基础操作 ====================
    
    def click(self, page: Page, name: str):
        """点击按钮"""
        page.click(self.get(name))
    
    def fill(self, page: Page, name: str, value: str):
        """填充表单字段"""
        page.fill(self.get(name), value)
    
    def select_option(self, page: Page, name: str, value: str):
        """选择下拉选项"""
        page.select_option(self.get(name), value)
    
    def wait_for_visible(self, page: Page, name: str, timeout: int = 30000):
        """等待元素可见"""
        page.wait_for_selector(self.get(name), state="visible", timeout=timeout)
    
    def wait_for_hidden(self, page: Page, name: str, timeout: int = 30000):
        """等待元素隐藏"""
        page.wait_for_selector(self.get(name), state="hidden", timeout=timeout)
    
    def is_visible(self, page: Page, name: str) -> bool:
        """检查元素是否可见"""
        return page.locator(self.get(name)).is_visible()
    
    def get_text(self, page: Page, name: str) -> str:
        """获取元素文本"""
        return page.locator(self.get(name)).inner_text()
    
    # ==================== 断言 ====================
    
    def expect_visible(self, page: Page, name: str):
        """断言元素可见"""
        expect(page.locator(self.get(name))).to_be_visible()
    
    def expect_hidden(self, page: Page, name: str):
        """断言元素隐藏"""
        expect(page.locator(self.get(name))).to_be_hidden()
    
    def expect_text(self, page: Page, name: str, text: str):
        """断言元素包含文本"""
        expect(page.locator(self.get(name))).to_contain_text(text)
    
    def expect_value(self, page: Page, name: str, value: str):
        """断言输入框的值"""
        expect(page.locator(self.get(name))).to_have_value(value)
    
    # ==================== Toast 处理 ====================
    
    def wait_for_toast(self, page: Page, timeout: int = 3000):
        """等待 toast 消息"""
        try:
            page.wait_for_selector(self.get('toast'), timeout=timeout)
            page.wait_for_timeout(500)
        except:
            pass
    
    def get_toast_text(self, page: Page) -> str:
        """获取 toast 消息文本"""
        return page.locator(self.get('toast')).inner_text()
    
    def expect_toast(self, page: Page, expected_text: str):
        """断言 toast 消息"""
        self.wait_for_toast(page)
        self.expect_text(page, 'toast', expected_text)
    
    def expect_error_toast(self, page: Page, error_key: str):
        """断言错误 toast（从配置文件读取错误消息）"""
        expected_text = self.error_msgs.get(error_key, error_key)
        self.expect_toast(page, expected_text)
    
    def expect_success_toast(self, page: Page, success_key: str):
        """断言成功 toast（从配置文件读取成功消息）"""
        expected_text = self.success_msgs.get(success_key, success_key)
        self.expect_toast(page, expected_text)
    
    # ==================== 错误字段处理 ====================
    
    def expect_field_error(self, page: Page, field_name: str, error_key: str):
        """断言字段错误提示"""
        error_selector = f"#error_{field_name}"
        expected_text = self.error_msgs.get(error_key, error_key)
        expect(page.locator(error_selector)).to_be_visible()
        expect(page.locator(error_selector)).to_contain_text(expected_text)


class SpecialSelectorManager(SelectorManager):
    """特殊选择器管理器 - 处理复杂场景"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.cascade_rules = config.get('cascade_rules', {})
    
    # ==================== 日期处理 ====================
    
    def set_date(self, page: Page, name: str, date_value: str):
        """设置日期（只读字段用 JS）"""
        selector = self.get(name)
        page.evaluate(f"document.querySelector('{selector}').value = '{date_value}';")
    
    def set_start_end_time(self, page: Page, start_time: str = '2024-01-01 10:00', 
                           end_time: str = '2024-01-01 18:00'):
        """设置开始和结束时间"""
        self.set_date(page, 'form_start_time', start_time)
        self.set_date(page, 'form_end_time', end_time)
    
    # ==================== 地点选择 ====================
    
    def select_online_location(self, page: Page):
        """选择线上地点"""
        page.click(self.get('location_type_online'))
    
    def select_offline_location(self, page: Page):
        """选择线下地点"""
        page.click(self.get('location_type_offline'))
    
    # ==================== 级联选择 ====================
    
    def select_cascade(self, page: Page, rule_name: str, value: str):
        """
        执行级联选择
        
        Args:
            page: Playwright page 对象
            rule_name: 级联规则名称（如 'city', 'district'）
            value: 要选择的值
        """
        rule = self.cascade_rules.get(rule_name)
        if not rule:
            raise ValueError(f"未找到级联规则: {rule_name}")
        
        # 选择父级
        parent_selector = self.get(rule['parent'])
        page.select_option(parent_selector, value)
        
        # 等待子级加载
        wait_condition = rule.get('wait_condition')
        if wait_condition:
            # 如果 wait_condition 是选择器名，转换为选择器
            if wait_condition in self.selectors:
                wait_condition = self.get(wait_condition)
            page.wait_for_selector(wait_condition, state="visible")
    
    def select_city(self, page: Page, province: str, city: str):
        """选择城市（先选省份，再选城市）"""
        # 选择省份
        page.select_option(self.get('form_province'), province)
        # 等待城市选项加载
        page.wait_for_selector(f"{self.get('form_city')} option:not([value=''])", state="visible")
        # 选择城市
        page.select_option(self.get('form_city'), city)
    
    def select_district(self, page: Page, district: str):
        """选择区县（需先选择城市）"""
        # 等待区县选项加载
        page.wait_for_selector(f"{self.get('form_district')} option:not([value=''])", state="visible")
        # 选择区县
        page.select_option(self.get('form_district'), district)
    
    def select_full_address(self, page: Page, province: str, city: str, district: str, address: str):
        """选择完整的省市区地址"""
        self.select_city(page, province, city)
        self.select_district(page, district)
        self.fill(page, 'form_address', address)
    
    # ==================== 子类型选择 ====================
    
    def select_activity_type(self, page: Page, activity_type: str):
        """选择活动类型并等待子类型加载"""
        self.select_option(page, 'form_type', activity_type)
        self.wait_for_visible(page, 'sub_type_div')
    
    def select_sub_type(self, page: Page, sub_type: str):
        """选择子类型"""
        self.select_option(page, 'form_sub_type', sub_type)
    
    # ==================== 文件上传 ====================
    
    def upload_file(self, page: Page, file_path: str):
        """上传文件"""
        selector = self.get('file_input')
        page.set_input_files(selector, file_path)
    
    def upload_temp_file(self, page: Page, suffix: str = ".pdf", content: str = "test content"):
        """创建临时文件并上传"""
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        try:
            self.upload_file(page, path)
        finally:
            os.remove(path)
    
    # ==================== 弹框处理 ====================
    
    def confirm_creation(self, page: Page):
        """确认创建（等待确认弹框并点击确认）"""
        self.wait_for_visible(page, 'confirm_modal')
        self.click(page, 'btn_confirm')
        self.wait_for_toast(page)
    
    def cancel_creation(self, page: Page, confirm: bool = True):
        """取消创建"""
        self.click(page, 'btn_cancel')
        if confirm:
            self.wait_for_visible(page, 'cancel_modal')
            self.click(page, 'btn_confirm')
        else:
            self.wait_for_hidden(page, 'cancel_modal')


# ==================== 工厂函数 ====================

def create_selector_manager(project: str = "activity") -> SelectorManager:
    """创建选择器管理器"""
    from test.ai.config import get_config
    config = get_config(project)
    return SelectorManager(config)


def create_special_selector_manager(project: str = "activity") -> SpecialSelectorManager:
    """创建特殊选择器管理器"""
    from test.ai.config import get_config
    config = get_config(project)
    return SpecialSelectorManager(config)