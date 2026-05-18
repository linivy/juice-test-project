# test/ai/generated/activity/test_create_activity.py
"""活动管理 - 创建活动模块自动化测试

基于需求文档: Requirements/活动管理_01_创建活动.md
测试框架: Playwright + pytest
前端: demo/activity_management.html
"""

import pytest
from playwright.sync_api import Page, expect

from test.ai.generated.activity.conftest import (
    BASE_URL,
    set_flatpickr_date,
    set_rich_text,
    fill_form_name,
    select_activity_type,
    select_sub_type,
    select_location_online,
    select_location_offline,
    fill_offline_address,
    clear_form_name,
    clear_activity_type,
    upload_attachment,
    submit_create,
    save_draft,
    discard_create,
    confirm_modal,
    cancel_modal_close,
    get_toast_text,
    get_error_text,
    is_modal_visible,
)


# ==================== P0: 正向流程 ====================


class TestCreateActivityPositive:
    """P0 - 正向流程：正常创建活动、保存草稿"""

    def test_create_activity_admin_online_with_attachment(
        self, create_modal_open: Page
    ):
        """TC-ACTIVITY-CREATE-001: Admin角色，填写所有必填字段，选择线上地点，
        上传附件，点击【完成创建】，确认后跳转列表页，显示"活动创建成功"toast"""
        page = create_modal_open

        # 1. 填写活动名称
        fill_form_name(page, "社区文化节")

        # 2. 选择活动类型：社区活动 → 运动会
        select_activity_type(page, "community")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "运动会")

        # 3. 设置活动时间（通过 flatpickr JS API）
        set_flatpickr_date(page, "#formStartTime", "2026-06-20 09:00")
        set_flatpickr_date(page, "#formEndTime", "2026-06-20 17:00")

        # 4. 选择线上地点，填写平台名称
        select_location_online(page)
        page.wait_for_selector("#formOnlinePlatform:not([style*='display: none'])", timeout=3000)
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 5. 填写活动简介（富文本编辑器）
        set_rich_text(page, "#formDescription",
            "<p>本次社区文化节旨在丰富居民文化生活，增进邻里感情。</p>")

        # 6. 上传附件
        upload_attachment(page, "test.pdf")

        # 7. 点击【完成创建】
        submit_create(page)
        page.wait_for_timeout(500)

        # 8. 确认弹框中点击【确认】
        page.wait_for_selector("#confirmModal.show", timeout=5000)
        confirm_modal(page)

        # 9. 验证 toast 消息
        toast_text = get_toast_text(page)
        assert "活动创建成功" in toast_text, f"期望 toast 包含'活动创建成功'，实际: {toast_text}"

    def test_save_draft_user_offline(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-002: 普通角色，填写所有必填字段，选择线下地点
        （省市区+详细地址），点击【保存】，保存为'活动待提交'状态，
        显示'草稿已保存，稍后可以继续编辑'toast"""
        page = create_modal_open

        # 切换到普通用户
        page.select_option("#roleSelect", "user1")
        page.wait_for_timeout(300)

        # 1. 填写活动名称
        fill_form_name(page, "亲子户外露营")

        # 2. 选择活动类型：家庭活动 → 户外露营
        select_activity_type(page, "family")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "户外露营")

        # 3. 设置活动时间
        set_flatpickr_date(page, "#formStartTime", "2026-07-01 08:00")
        set_flatpickr_date(page, "#formEndTime", "2026-07-03 18:00")

        # 4. 选择线下地点，填写省市区和详细地址
        select_location_offline(page)
        page.wait_for_selector("#offlineLocation:not([style*='display: none'])", timeout=3000)
        fill_offline_address(page, "广东省", "深圳市", "南山区", "深圳湾公园")

        # 5. 填写活动简介
        set_rich_text(page, "#formDescription", "<p>亲子户外露营活动，亲近自然。</p>")

        # 6. 点击【保存草稿】
        save_draft(page)

        # 7. 验证 toast
        toast_text = get_toast_text(page)
        assert "草稿已保存" in toast_text, f"期望 toast 包含'草稿已保存'，实际: {toast_text}"

    def test_save_draft_name_only(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-003: 仅填写活动名称，点击【保存】，
        保存为'活动待提交'状态，显示'草稿已保存'toast"""
        page = create_modal_open

        # 1. 仅填写活动名称
        fill_form_name(page, "未完成的测试活动")

        # 2. 点击【保存草稿】
        save_draft(page)

        # 3. 验证 toast
        toast_text = get_toast_text(page)
        assert "草稿已保存" in toast_text, f"期望 toast 包含'草稿已保存'，实际: {toast_text}"


# ==================== P1: 必填字段校验 ====================


class TestCreateActivityValidation:
    """P1 - 必填字段校验"""

    def test_all_fields_empty(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-004: 所有必填字段为空，点击【完成创建】，
        预期提示'请输入活动名称'"""
        page = create_modal_open

        # 所有字段保持为空，直接点击提交
        submit_create(page)
        page.wait_for_timeout(500)

        # 验证活动名称错误提示（页面验证顺序第一项）
        error_text = get_error_text(page, "formName")
        assert "请输入活动名称" in error_text, \
            f"期望错误'请输入活动名称'，实际: {error_text}"

    def test_name_empty_others_valid(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-005: 仅活动名称为空，其他必填字段完整，
        点击【完成创建】，提示'请输入活动名称'"""
        page = create_modal_open

        # 填写除活动名称外的所有必填字段
        select_activity_type(page, "community")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "知识讲座")
        set_flatpickr_date(page, "#formStartTime", "2026-06-15 10:00")
        set_flatpickr_date(page, "#formEndTime", "2026-06-15 12:00")
        set_rich_text(page, "#formDescription", "<p>测试简介</p>")

        # 点击提交
        submit_create(page)
        page.wait_for_timeout(500)

        # 验证错误提示
        error_text = get_error_text(page, "formName")
        assert "请输入活动名称" in error_text, \
            f"期望错误'请输入活动名称'，实际: {error_text}"

    def test_type_empty_others_valid(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-006: 仅活动类型为空，其他必填字段完整，
        点击【完成创建】，提示'请选择活动类型'"""
        page = create_modal_open

        # 填写除活动类型外的必填字段
        fill_form_name(page, "测试活动名称")
        set_flatpickr_date(page, "#formStartTime", "2026-06-15 10:00")
        set_flatpickr_date(page, "#formEndTime", "2026-06-15 12:00")
        set_rich_text(page, "#formDescription", "<p>测试简介</p>")

        # 点击提交
        submit_create(page)
        page.wait_for_timeout(500)

        # 验证错误提示
        error_text = get_error_text(page, "formType")
        assert "请选择活动类型" in error_text, \
            f"期望错误'请选择活动类型'，实际: {error_text}"

    def test_start_time_empty_others_valid(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-007: 仅活动时间为空，其他必填字段完整，
        点击【完成创建】，提示'请选择开始时间'"""
        page = create_modal_open

        # 填写除开始时间外的必填字段
        fill_form_name(page, "测试活动名称")
        select_activity_type(page, "community")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "才艺比赛")
        # 不设置开始时间，只设置结束时间
        set_flatpickr_date(page, "#formEndTime", "2026-06-15 12:00")
        set_rich_text(page, "#formDescription", "<p>测试简介</p>")

        # 点击提交
        submit_create(page)
        page.wait_for_timeout(500)

        # 验证错误提示
        error_text = get_error_text(page, "formStartTime")
        assert "请选择开始时间" in error_text, \
            f"期望错误'请选择开始时间'，实际: {error_text}"

    def test_description_empty_others_valid(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-008: 仅活动简介为空，其他必填字段完整，
        点击【完成创建】，提示'请输入活动简介'"""
        page = create_modal_open

        # 填写除活动简介外的必填字段
        fill_form_name(page, "测试活动名称")
        select_activity_type(page, "family")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "亲子活动")
        set_flatpickr_date(page, "#formStartTime", "2026-06-15 10:00")
        set_flatpickr_date(page, "#formEndTime", "2026-06-15 12:00")
        # 不填写活动简介

        # 点击提交
        submit_create(page)
        page.wait_for_timeout(500)

        # 验证错误提示
        error_text = get_error_text(page, "formDescription")
        assert "请输入活动简介" in error_text, \
            f"期望错误'请输入活动简介'，实际: {error_text}"


# ==================== P0: 级联联动 ====================


class TestCreateActivityCascade:
    """P0 - 活动类型与地点的级联联动"""

    def test_type_community_shows_sub_options(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-009: 选择活动类型'社区活动'，
        二级下拉框显示'运动会'/'知识讲座'/'才艺比赛'"""
        page = create_modal_open

        # 选择社区活动
        select_activity_type(page, "community")
        page.wait_for_timeout(300)

        # 验证二级下拉框可见
        sub_type_div = page.locator("#subTypeDiv")
        expect(sub_type_div).to_be_visible()

        # 验证二级选项
        sub_type_select = page.locator("#formSubType")
        options = sub_type_select.locator("option").all_inner_texts()
        # 过滤掉"请选择子类型"默认选项
        real_options = [o for o in options if o != "请选择子类型"]

        expected_options = ["运动会", "知识讲座", "才艺比赛"]
        for expected in expected_options:
            assert expected in real_options, \
                f"期望二级选项包含'{expected}'，实际选项: {real_options}"

    def test_type_family_shows_sub_options(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-010: 选择活动类型'家庭活动'，
        二级下拉框显示'亲子活动'/'户外露营'/'亲子烘焙'"""
        page = create_modal_open

        # 选择家庭活动
        select_activity_type(page, "family")
        page.wait_for_timeout(300)

        # 验证二级下拉框可见
        sub_type_div = page.locator("#subTypeDiv")
        expect(sub_type_div).to_be_visible()

        # 验证二级选项
        sub_type_select = page.locator("#formSubType")
        options = sub_type_select.locator("option").all_inner_texts()
        real_options = [o for o in options if o != "请选择子类型"]

        expected_options = ["亲子活动", "户外露营", "亲子烘焙"]
        for expected in expected_options:
            assert expected in real_options, \
                f"期望二级选项包含'{expected}'，实际选项: {real_options}"

    def test_type_other_hides_sub_shows_input(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-011: 选择活动类型'其他'，
        二级下拉框消失，显示'活动类型说明'文本输入框"""
        page = create_modal_open

        # 选择"其他"
        select_activity_type(page, "other")
        page.wait_for_timeout(300)

        # 验证二级下拉框隐藏
        sub_type_div = page.locator("#subTypeDiv")
        expect(sub_type_div).to_be_hidden()

        # 验证"活动类型说明"输入框可见
        other_type_input = page.locator("#formOtherType")
        expect(other_type_input).to_be_visible()

        # 验证可以输入（必填，限50字符）
        page.fill("#formOtherType", "自定义活动类型说明")
        value = page.input_value("#formOtherType")
        assert value == "自定义活动类型说明", f"期望值'自定义活动类型说明'，实际: {value}"

    def test_location_online_shows_platform(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-012: 选择活动地点'线上'，
        显示'平台名称'输入框，省市区地址隐藏"""
        page = create_modal_open

        # 选择线上地点
        select_location_online(page)
        page.wait_for_timeout(300)

        # 验证平台名称输入框可见
        platform_input = page.locator("#formOnlinePlatform")
        expect(platform_input).to_be_visible()

        # 验证省市区字段隐藏
        offline_div = page.locator("#offlineLocation")
        expect(offline_div).to_be_hidden()

    def test_location_offline_shows_address(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-013: 选择活动地点'线下'，
        显示省市区下拉框 + '详细地址'输入框，平台名称隐藏"""
        page = create_modal_open

        # 选择线下地点
        select_location_offline(page)
        page.wait_for_timeout(300)

        # 验证省市区下拉框可见
        offline_div = page.locator("#offlineLocation")
        expect(offline_div).to_be_visible()

        # 验证平台名称隐藏
        online_div = page.locator("#onlineLocation")
        expect(online_div).to_be_hidden()

        # 验证可以填写省市区和详细地址
        fill_offline_address(page, "广东省", "深圳市", "南山区", "科技园")
        # 验证省份已选择
        province_value = page.input_value("#formProvince")
        assert province_value != "", "期望省份已选择"


# ==================== P1: 放弃创建 ====================


class TestCreateActivityDiscard:
    """P1 - 放弃创建操作"""

    def test_discard_confirm(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-014: 填写部分信息后，点击【放弃创建】，
        确认放弃，返回列表页，填写的信息不保存"""
        page = create_modal_open

        # 填写部分信息
        fill_form_name(page, "会被放弃的活动")
        select_activity_type(page, "community")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "知识讲座")

        # 点击【放弃创建】
        discard_create(page)
        page.wait_for_timeout(300)

        # 确认放弃弹窗应出现
        page.wait_for_selector("#confirmModal.show", timeout=5000)

        # 点击确认
        confirm_modal(page)

        # 验证返回列表页，创建弹窗关闭
        page.wait_for_timeout(500)
        list_page = page.locator("#listPage")
        expect(list_page).to_be_visible()
        assert not is_modal_visible(page, "createModal"), "创建弹窗应该已关闭"

    def test_discard_cancel(self, create_modal_open: Page):
        """TC-ACTIVITY-CREATE-015: 填写部分信息后，点击【放弃创建】，
        取消放弃，停留在创建弹框上，已填写的信息保留"""
        page = create_modal_open

        # 填写部分信息
        activity_name = "不会放弃的活动"
        fill_form_name(page, activity_name)
        select_activity_type(page, "family")
        page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
        select_sub_type(page, "亲子烘焙")

        # 点击【放弃创建】
        discard_create(page)
        page.wait_for_timeout(300)

        # 确认弹窗出现
        page.wait_for_selector("#confirmModal.show", timeout=5000)

        # 点击取消
        cancel_modal_close(page)

        # 验证停留在创建弹窗
        page.wait_for_timeout(500)
        assert is_modal_visible(page, "createModal"), "创建弹窗应该仍然可见"

        # 验证已填写的信息保留
        current_name = page.input_value("#formName")
        assert current_name == activity_name, \
            f"期望活动名称保留为'{activity_name}'，实际: {current_name}"
