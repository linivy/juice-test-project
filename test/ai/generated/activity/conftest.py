# test/ai/generated/activity/conftest.py
"""活动管理测试专用 fixtures"""
import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:5000"


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
    page.wait_for_selector("#listPage", timeout=10000)
    return page


@pytest.fixture
def create_modal_open(activity_page: Page):
    """打开创建活动弹窗"""
    page = activity_page
    page.click("#btnCreate")
    page.wait_for_selector("#createModal.show", timeout=5000)
    return page


# ==================== 表单操作工具函数 ====================


def set_flatpickr_date(page: Page, selector: str, date_str: str):
    """通过 JavaScript 设置 flatpickr 日期

    Args:
        page: Playwright Page
        selector: 日期选择器的 CSS 选择器（如 '#formStartTime'）
        date_str: 日期字符串，格式 'YYYY-MM-DD HH:MM'（如 '2026-06-01 09:00'）
    """
    # 先点击输入框获取焦点
    page.locator(selector).click()
    page.wait_for_timeout(300)
    # 通过 flatpickr 实例设置日期
    page.evaluate(
        """([sel, date]) => {
            const el = document.querySelector(sel);
            if (el && el._flatpickr) {
                el._flatpickr.setDate(date);
            }
        }""",
        [selector, date_str],
    )
    # 关闭可能弹出的日历
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)


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
    page.fill("#formName", name)


def select_activity_type(page: Page, type_value: str):
    """选择活动类型

    Args:
        type_value: 'community', 'family', 或 'other'
    """
    page.select_option("#formType", type_value)
    page.wait_for_timeout(300)


def select_sub_type(page: Page, sub_type: str):
    """选择子类型"""
    page.select_option("#formSubType", sub_type)
    page.wait_for_timeout(200)


def select_location_online(page: Page):
    """选择线上地点"""
    page.check("input[name='locationType'][value='online']")
    page.wait_for_timeout(300)


def select_location_offline(page: Page):
    """选择线下地点"""
    page.check("input[name='locationType'][value='offline']")
    page.wait_for_timeout(300)


def fill_offline_address(page: Page, province: str, city: str, district: str, address: str):
    """填写线下地址（省市区 + 详细地址）"""
    # 选择省份
    page.select_option("#formProvince", province)
    page.wait_for_timeout(500)
    # 选择城市
    page.select_option("#formCity", city)
    page.wait_for_timeout(500)
    # 选择区
    page.select_option("#formDistrict", district)
    page.wait_for_timeout(300)
    # 填写详细地址
    page.fill("#formAddress", address)


def clear_form_name(page: Page):
    """清空活动名称"""
    page.fill("#formName", "")


def clear_activity_type(page: Page):
    """重置活动类型"""
    page.select_option("#formType", "")
    page.wait_for_timeout(200)


def upload_attachment(page: Page, file_path: str):
    """上传附件"""
    page.set_input_files("#fileInput", file_path)
    page.wait_for_timeout(500)


def submit_create(page: Page):
    """点击【完成创建】按钮"""
    page.click("#btnSubmit")


def save_draft(page: Page):
    """点击【保存草稿】按钮"""
    page.click("#btnSaveDraft")


def discard_create(page: Page):
    """点击【放弃创建】按钮"""
    page.click("#btnCancel")


def confirm_modal(page: Page):
    """在确认弹框中点击确认"""
    page.click("#confirmModal #btnConfirm")
    page.wait_for_timeout(300)


def cancel_modal_close(page: Page):
    """在确认弹框中点击取消/关闭"""
    page.click("#btnConfirmCancelBtn")
    page.wait_for_timeout(300)


def get_toast_text(page: Page) -> str:
    """获取 toast 消息文本"""
    toast = page.locator("#toast")
    toast.wait_for(state="visible", timeout=5000)
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
