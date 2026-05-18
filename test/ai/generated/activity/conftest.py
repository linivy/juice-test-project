# test/ai/generated/activity/conftest.py
"""活动管理测试专用 fixtures — 从 config/activity.yaml 读取所有选择器和超时配置"""

import pytest
import yaml
from pathlib import Path
from playwright.sync_api import Page

# ==================== 配置加载 ====================

_CFG_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "activity.yaml"
with open(_CFG_PATH, encoding="utf-8") as _f:
    _cfg = yaml.safe_load(_f)

SEL = _cfg["selectors"]                   # 选择器映射
TMO = _cfg.get("timeouts", {})            # 超时配置
BASE_URL = _cfg.get("base_url", "http://localhost:5000")

# ==================== Fixtures ====================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def activity_page(page: Page):
    """打开活动管理页面并准备好创建活动的 fixture"""
    page.goto(BASE_URL, wait_until="networkidle")
    page.wait_for_selector(SEL["list_page"], timeout=TMO.get("page_load", 10000))
    return page


@pytest.fixture
def create_modal_open(activity_page: Page):
    """打开创建活动弹窗"""
    page = activity_page
    page.click(SEL["btn_create"])
    page.wait_for_selector(
        f"{SEL['create_modal']}.show",
        timeout=TMO.get("modal_show", 5000),
    )
    return page


# ==================== 表单操作工具函数 ====================


def set_flatpickr_date(page: Page, selector: str, date_str: str):
    """通过 JavaScript 设置 flatpickr 日期

    Args:
        page: Playwright Page
        selector: 日期选择器的 CSS 选择器（如 '#formStartTime'）
        date_str: 日期字符串，格式 'YYYY-MM-DD HH:MM'（如 '2026-06-01 09:00'）
    """
    page.locator(selector).click()
    page.wait_for_timeout(TMO.get("ui_transition", 300))
    page.evaluate(
        """([sel, date]) => {
            const el = document.querySelector(sel);
            if (el && el._flatpickr) {
                el._flatpickr.setDate(date);
            }
        }""",
        [selector, date_str],
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(TMO.get("ui_short", 200))


def set_rich_text(page: Page, selector: str, html_content: str):
    """设置富文本编辑器（contenteditable 元素）的内容

    Args:
        page: Playwright Page
        selector: 富文本编辑器的 CSS 选择器（如 '#formDescription'）
        html_content: HTML 内容字符串
    """
    page.evaluate(
        """([sel, html]) => {
            const el = document.querySelector(sel);
            if (el) {
                el.innerHTML = html;
                el.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }""",
        [selector, html_content],
    )


def fill_form_name(page: Page, name: str):
    """填写活动名称"""
    page.fill(SEL["form_name"], name)


def select_activity_type(page: Page, type_value: str):
    """选择活动类型

    Args:
        type_value: 'community', 'family', 或 'other'
    """
    page.select_option(SEL["form_type"], type_value)
    page.wait_for_timeout(TMO.get("ui_transition", 300))


def select_sub_type(page: Page, sub_type: str):
    """选择子类型"""
    page.select_option(SEL["form_sub_type"], sub_type)
    page.wait_for_timeout(TMO.get("ui_short", 200))


def select_location_online(page: Page):
    """选择线上地点"""
    page.check(SEL["location_type_online"])
    page.wait_for_timeout(TMO.get("ui_transition", 300))


def select_location_offline(page: Page):
    """选择线下地点"""
    page.check(SEL["location_type_offline"])
    page.wait_for_timeout(TMO.get("ui_transition", 300))


def fill_offline_address(page: Page, province: str, city: str, district: str, address: str):
    """填写线下地址（省市区 + 详细地址）"""
    page.select_option(SEL["form_province"], province)
    page.wait_for_timeout(TMO.get("cascade_api", 500))
    page.select_option(SEL["form_city"], city)
    page.wait_for_timeout(TMO.get("cascade_api", 500))
    page.select_option(SEL["form_district"], district)
    page.wait_for_timeout(TMO.get("ui_transition", 300))
    page.fill(SEL["form_address"], address)


def clear_form_name(page: Page):
    """清空活动名称"""
    page.fill(SEL["form_name"], "")


def clear_activity_type(page: Page):
    """重置活动类型"""
    page.select_option(SEL["form_type"], "")
    page.wait_for_timeout(TMO.get("ui_short", 200))


def upload_attachment(page: Page, file_path: str):
    """上传附件"""
    page.set_input_files(SEL["file_input"], file_path)
    page.wait_for_timeout(TMO.get("file_upload", 500))


def submit_create(page: Page):
    """点击【完成创建】按钮"""
    page.click(SEL["btn_submit"])


def save_draft(page: Page):
    """点击【保存草稿】按钮"""
    page.click(SEL["btn_save_draft"])


def discard_create(page: Page):
    """点击【放弃创建】按钮"""
    page.click(SEL["btn_cancel"])


def confirm_modal(page: Page):
    """在确认弹框中点击确认"""
    page.click(SEL["btn_confirm"])
    page.wait_for_timeout(TMO.get("ui_transition", 300))


def cancel_modal_close(page: Page):
    """在确认弹框中点击取消/关闭"""
    page.click(SEL["btn_confirm_cancel_btn"])
    page.wait_for_timeout(TMO.get("ui_transition", 300))


def get_toast_text(page: Page) -> str:
    """获取 toast 消息文本"""
    toast = page.locator(SEL["toast"])
    toast.wait_for(state="visible", timeout=TMO.get("toast_visible", 5000))
    return toast.inner_text()


def get_error_text(page: Page, field_id: str) -> str:
    """获取字段错误提示文本"""
    error_sel = f"#error_{field_id}"
    error_el = page.locator(error_sel)
    if error_el.is_visible():
        return error_el.inner_text()
    return ""


def is_modal_visible(page: Page, modal_id: str) -> bool:
    """检查指定弹窗是否可见"""
    return page.locator(f"#{modal_id}.show").is_visible()
