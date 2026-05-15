# -*- coding: utf-8 -*-
"""
AI 生成的自动化测试用例
================================
生成时间: 2026-05-15 13:12:22
需求: Requirements/活动管理_01_创建活动.md
模块: activity
功能: activity
"""

import pytest
import allure
from playwright.sync_api import expect

BASE_URL = "http://localhost:5000"

class TestActivity:
    """创建活动功能测试自动生成"""

    def navigate_to_page(self, page):
        """导航到页面"""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

    def wait_for_toast(self, page, timeout=3000):
        """等待toast消息"""
        try:
            page.wait_for_selector("#toast", timeout=timeout)
            page.wait_for_timeout(500)
        except:
            pass

    def close_dialog(self, page):
        """关闭弹窗"""
        try:
            page.locator(".modal-close, .dialog-close, #btnCloseModal").click(timeout=2000)
        except:
            pass
    @allure.feature("创建活动")
    @allure.title("TC_001: 测试Admin角色填写所有必填字段（活动名称、活动类型、活动时间、活动简介），选择线上地点并上传附件，点击【完成创建】，验证弹出确认弹框，确认后跳转列表页并显示“活动创建成功”toast")
    def test_TC_001(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.set_input_files("input[type='file']", "test.pdf")
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_002: 测试普通角色填写所有必填字段，选择线下地点（省市区+详细地址），点击【保存】，验证保存为“活动待提交”状态，跳转列表页并显示“草稿已保存，稍后可以继续编辑”toast")
    def test_TC_002(self, page):
        # 1. 导航到活动页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写必填字段（活动名称、活动类型）
        page.fill("#formName", "测试线下活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 4. 选择线下地点
        page.click('input[name="locationType"][value="offline"]')
        page.select_option("#formProvince", "广东省")
        page.select_option("#formCity", "深圳市")
        page.select_option("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园南区A栋")

        # 5. 点击保存草稿按钮（只验证活动名称和活动类型）
        page.click("#btnSaveDraft")

        # 6. 验证toast消息
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("草稿已保存，稍后可以继续编辑")
        expect(page.locator("#toast")).to_be_visible()

        # 7. 验证跳转到列表页并显示草稿状态
        expect(page.locator("#activityTableBody")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_003: 测试仅填写活动名称，点击【保存】，验证保存为“活动待提交”状态，跳转列表页并显示“草稿已保存”toast")
    def test_TC_003(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 仅填写活动名称
        page.fill("#formName", "测试活动名称")

        # 5. 点击保存草稿按钮
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.click("#btnSaveDraft")

        # 6. 验证toast消息
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("草稿已保存")

        # 7. 验证跳转到列表页（检查列表页元素可见）
        expect(page.locator("#activityTableBody")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_004: 测试选择活动类型“社区活动”，验证二级下拉框显示“运动会”/“知识讲座”/“才艺比赛”")
    def test_TC_004(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建活动按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 选择活动类型为"社区活动"
        page.select_option("#formType", "community")

        # 5. 等待二级下拉框出现
        page.wait_for_selector("#subTypeDiv", state="visible")

        # 6. 验证二级下拉框包含"运动会"、"知识讲座"、"才艺比赛"选项
        sub_type_options = page.locator("#formSubType option").all_text_contents()
        assert "运动会" in sub_type_options, "二级下拉框应包含'运动会'选项"
        assert "知识讲座" in sub_type_options, "二级下拉框应包含'知识讲座'选项"
        assert "才艺比赛" in sub_type_options, "二级下拉框应包含'才艺比赛'选项"

        # 7. 选择"运动会"验证可选
        page.select_option("#formSubType", "运动会")

        # 8. 填写其他必填字段以完成表单（可选，用于验证流程完整性）
        page.fill("#formName", "测试社区活动")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个社区活动测试")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 9. 提交表单
        page.click("#btnSubmit")

        # 10. 等待确认弹框并确认
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")

        # 11. 等待并验证成功消息
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_005: 测试选择活动类型“家庭活动”，验证二级下拉框显示“亲子活动”/“户外露营”/“亲子烘焙”")
    def test_TC_005(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试家庭活动")
        page.select_option("#formType", "family")
        page.wait_for_selector("#subTypeDiv", state="visible")
        # 验证二级下拉框包含所有预期选项
        sub_type_options = page.locator("#formSubType option").all_text_contents()
        expected_options = ["亲子活动", "户外露营", "亲子烘焙"]
        for option in expected_options:
            assert option in sub_type_options, f"二级下拉框缺少选项: {option}"
            page.select_option("#formSubType", "亲子活动")
            page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
            page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
            page.fill("#formDescription", "这是一个家庭活动测试")
            page.click('input[name="locationType"][value="online"]')
            page.fill("#formOnlinePlatform", "腾讯会议")
            page.click("#btnSubmit")
            page.wait_for_selector("#confirmModal", state="visible")
            page.click("#btnConfirm")
            self.wait_for_toast(page)
            expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_006: 测试选择活动类型“其他”，验证二级下拉框消失，显示“活动类型说明”文本输入框（必填，限50字符）")
    def test_TC_006(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 选择活动类型为"其他"
        page.select_option("#formType", "other")

        # 4. 验证二级下拉框消失
        page.wait_for_selector("#subTypeDiv", state="hidden")

        # 5. 验证"活动类型说明"文本输入框显示
        expect(page.locator("#formOtherType")).to_be_visible()

        # 6. 填写活动类型说明（必填，限50字符）
        page.fill("#formOtherType", "这是一个自定义活动类型说明")

        # 7. 填写其他必填字段
        page.fill("#formName", "测试活动")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 8. 点击提交按钮
        page.click("#btnSubmit")

        # 9. 等待确认弹框并确认
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")

        # 10. 验证成功消息
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_007: 测试选择活动地点“线上”，验证显示“平台名称”输入框（限50字符），省市区地址隐藏")
    def test_TC_007(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写表单（填写所有必填字段）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")

        # 4. 选择线上模式
        page.click('input[name="locationType"][value="online"]')

        # 5. 验证平台名称输入框可见
        expect(page.locator("#formOnlinePlatform")).to_be_visible()

        # 6. 验证省市区地址隐藏
        expect(page.locator("#formProvince")).not_to_be_visible()
        expect(page.locator("#formCity")).not_to_be_visible()
        expect(page.locator("#formDistrict")).not_to_be_visible()
        expect(page.locator("#formAddress")).not_to_be_visible()

        # 7. 填写平台名称（限50字符）
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 8. 点击提交
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_008: 测试选择活动地点“线下”，验证显示省市区下拉框 + “详细地址”输入框（限50字符），平台名称隐藏")
    def test_TC_008(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写表单（填写所有必填字段）
        page.fill("#formName", "测试线下活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个线下活动测试")

        # 4. 选择线下模式
        page.click('input[name="locationType"][value="offline"]')

        # 5. 验证省市区下拉框和详细地址输入框可见
        expect(page.locator("#formProvince")).to_be_visible()
        expect(page.locator("#formCity")).to_be_visible()
        expect(page.locator("#formDistrict")).to_be_visible()
        expect(page.locator("#formAddress")).to_be_visible()

        # 6. 验证平台名称输入框隐藏
        expect(page.locator("#formOnlinePlatform")).to_be_hidden()

        # 7. 选择省市区
        page.select_option("#formProvince", "广东省")
        page.select_option("#formCity", "深圳市")
        page.select_option("#formDistrict", "南山区")

        # 8. 填写详细地址（限50字符）
        page.fill("#formAddress", "科技园南区A栋")

        # 9. 提交表单
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_009: 测试活动名称为空")
    def test_TC_009(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_010: 测试所有必填字段为空，点击【完成创建】，验证弹出提示“活动信息未完善，请前往完善”")
    def test_TC_010(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("活动信息未完善，请前往完善")
    @allure.feature("创建活动")
    @allure.title("TC_011: 测试仅活动名称为空，其他必填字段完整，点击【完成创建】，验证提示“请输入活动名称”，活动名称字段显示错误“请输入活动名称”")
    def test_TC_011(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        # 活动名称留空
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_012: 测试仅活动类型为空，其他必填字段完整，点击【完成创建】，验证提示“请选择活动类型”，活动类型字段显示错误“请选择活动类型”")
    def test_TC_012(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写表单（活动类型留空）
        page.fill("#formName", "测试活动")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 4. 点击完成创建
        page.click("#btnSubmit")

        # 5. 验证错误提示
        expect(page.locator("#toast")).to_contain_text("请选择活动类型")
        expect(page.locator("#error_formType")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_013: 测试仅活动时间为空，其他必填字段完整，点击【完成创建】，验证提示“选择开始时间”，开始时间字段显示错误“选择开始时间”")
    def test_TC_013(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 填写表单 - 所有必填字段除了开始时间
        # 活动名称
        page.fill("#formName", "测试活动")

        # 活动类型 - 选择社区活动
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 活动时间 - 只填写结束时间，不填写开始时间
        # 开始时间留空
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")

        # 活动简介
        page.fill("#formDescription", "这是一个测试活动")

        # 地点模式 - 选择线上
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 5. 点击【完成创建】按钮
        page.click("#btnSubmit")

        # 6. 验证错误提示
        # Toast 消息验证
        expect(page.locator("#toast")).to_contain_text("请选择开始时间")
        expect(page.locator("#toast")).to_be_visible()

        # 开始时间字段错误提示验证
        expect(page.locator("#error_formStartTime")).to_be_visible()
        expect(page.locator("#error_formStartTime")).to_contain_text("请选择开始时间")
    @allure.feature("创建活动")
    @allure.title("TC_014: 测试仅活动简介为空，其他必填字段完整，点击【完成创建】，验证提示“请输入活动简介”，活动简介字段显示错误“请输入活动简介”")
    def test_TC_014(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写活动名称
        page.fill("#formName", "测试活动")

        # 4. 选择活动类型（社区活动）
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 5. 设置活动时间
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")

        # 6. 选择线上模式
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 7. 活动简介留空，点击【完成创建】
        page.click("#btnSubmit")

        # 8. 验证toast提示
        expect(page.locator("#toast")).to_contain_text("请输入活动简介")

        # 9. 验证活动简介字段显示错误
        expect(page.locator("#error_formDescription")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_015: 测试填写部分信息后，点击【放弃创建】，确认放弃，验证返回列表页，填写的信息不保存")
    def test_TC_015(self, page):
        # 1. 导航到活动列表页
        self.navigate_to_page(page)

        # 2. 点击创建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写部分信息（活动名称和活动类型）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 4. 点击放弃创建按钮
        page.click("#btnCancel")

        # 5. 等待确认放弃弹框出现并确认放弃
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")

        # 6. 验证返回列表页（创建弹框关闭）
        page.wait_for_selector("#createModal", state="hidden")

        # 7. 验证列表页没有新增的活动记录（填写的信息不保存）
        expect(page.locator("#activityTableBody")).not_to_contain_text("测试活动")
    @allure.feature("创建活动")
    @allure.title("TC_016: 测试填写部分信息后，点击【放弃创建】，取消放弃，验证停留在创建页，已填写的信息保留")
    def test_TC_016(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写部分信息
        page.fill("#formName", "测试活动名称")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动简介")

        # 4. 点击放弃创建按钮（假设存在，根据实际页面元素调整）
        page.click("#btnCancel")

        # 5. 等待取消确认弹框出现
        page.wait_for_selector("#confirmModal", state="visible")

        # 6. 点击取消放弃（即点击取消按钮）
        page.click("#btnCancel")

        # 7. 验证停留在创建页
        expect(page.locator("#createModal")).to_be_visible()

        # 8. 验证已填写的信息保留
        expect(page.locator("#formName")).to_have_value("测试活动名称")
        expect(page.locator("#formType")).to_have_value("社区活动")
        expect(page.locator("#formSubType")).to_have_value("运动会")
        expect(page.locator("#formStartTime")).to_have_value("2024-01-01 10:00")
        expect(page.locator("#formEndTime")).to_have_value("2024-01-01 18:00")
        expect(page.locator("#formDescription")).to_have_value("这是一个测试活动简介")
    @allure.feature("创建活动")
    @allure.title("TC_017: 测试活动名称为空")
    def test_TC_017(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_018: 测试活动类型被停用后，点击【完成创建】，验证弹出提示“所选活动类型已被停用，请选择新的活动类型”")
    def test_TC_018(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        # 模拟活动类型被停用（通过 JavaScript 修改 select 选项的 disabled 属性）
        page.evaluate("document.querySelector('#formType option[value=\"社区活动\"]').disabled = true;")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("所选活动类型已被停用，请选择新的活动类型")
        expect(page.locator("#toast")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_019: 测试重复快速点击【完成创建】按钮，验证只创建一次活动，不产生重复数据")
    def test_TC_019(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写表单
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 4. 快速重复点击【完成创建】按钮
        page.click("#btnSubmit")
        page.click("#btnSubmit")
        page.click("#btnSubmit")

        # 5. 等待确认弹框出现
        page.wait_for_selector("#confirmModal", state="visible")

        # 6. 点击确认
        page.click("#btnConfirm")

        # 7. 等待 toast 消息
        self.wait_for_toast(page)

        # 8. 验证只创建一次活动，不产生重复数据
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
        expect(page.locator("#toast")).to_be_visible()

        # 9. 验证活动列表中只有一条记录
        page.wait_for_selector("#activityTableBody", state="visible")
        assert page.locator("#activityTableBody tr").count() == 1
    @allure.feature("创建活动")
    @allure.title("TC_020: 测试活动名称为空")
    def test_TC_020(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.select_option("#formType", "community")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

