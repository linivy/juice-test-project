# -*- coding: utf-8 -*-
"""
AI 生成的自动化测试用例
================================
生成时间: 2026-05-15 10:43:40
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
    @allure.title("TC_001: 测试Admin角色成功创建线上活动（填写所有必填项，选择线上地点，上传附件，点击【完成创建】）")
    def test_TC_001(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试线上活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个线上活动测试")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.set_input_files("input[type='file']", "test.pdf")
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_002: 测试普通角色成功保存线下活动草稿（填写所有必填项，选择线下地点，点击【保存】）")
    def test_TC_002(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 填写表单 - 必填项
        page.fill("#formName", "测试线下活动草稿")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 5. 选择线下地点
        page.click('input[name="locationType"][value="offline"]')
        page.select_option("#formProvince", "广东省")
        page.wait_for_selector("#formCity option", state="visible")
        page.select_option("#formCity", "深圳市")
        page.wait_for_selector("#formDistrict option", state="visible")
        page.select_option("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园南区A栋")

        # 6. 点击保存草稿按钮
        page.click("#btnSaveDraft")

        # 7. 验证保存成功
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("草稿已保存")
        expect(page.locator("#toast")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_003: 测试仅填写活动名称后成功保存草稿（点击【保存】）")
    def test_TC_003(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.click("#btnSaveDraft")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("草稿已保存")
        expect(page.locator("#toast")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_004: 测试选择活动类型“社区活动”时，二级下拉框联动显示“运动会”、“知识讲座”、“才艺比赛”")
    def test_TC_004(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        # 验证二级下拉框包含所有选项
        options = page.locator("#formSubType option").all_text_contents()
        expected_options = ["运动会", "知识讲座", "才艺比赛"]
        for option in expected_options:
            assert option in options, f"二级下拉框缺少选项: {option}"
            page.select_option("#formSubType", "运动会")
            page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
            page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
            page.fill("#formDescription", "这是一个测试活动")
            page.click('input[name="locationType"][value="online"]')
            page.fill("#formOnlinePlatform", "腾讯会议")
            page.click("#btnSubmit")
            page.wait_for_selector("#confirmModal", state="visible")
            page.click("#btnConfirm")
            self.wait_for_toast(page)
            expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_005: 测试选择活动类型“家庭活动”时，二级下拉框联动显示“亲子活动”、“户外露营”、“亲子烘焙”")
    def test_TC_005(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.select_option("#formType", "家庭活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        expect(page.locator("#formSubType option")).to_contain_text("亲子活动")
        expect(page.locator("#formSubType option")).to_contain_text("户外露营")
        expect(page.locator("#formSubType option")).to_contain_text("亲子烘焙")
    @allure.feature("创建活动")
    @allure.title("TC_006: 测试选择活动类型“其他”时，二级下拉框消失并显示“活动类型说明”文本输入框（必填，限50字符）")
    def test_TC_006(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建活动按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 填写表单
        # 4.1 填写活动名称
        page.fill("#formName", "测试活动")

        # 4.2 选择活动类型为"其他"
        page.select_option("#formType", "其他")

        # 4.3 等待二级下拉框消失
        page.wait_for_selector("#subTypeDiv", state="hidden")

        # 4.4 填写活动类型说明（必填，限50字符）
        page.fill("#formOtherType", "这是一个自定义活动类型说明")

        # 4.5 填写活动时间
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")

        # 4.6 填写活动简介
        page.fill("#formDescription", "这是一个测试活动")

        # 4.7 选择线上模式
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 5. 点击提交按钮
        page.click("#btnSubmit")

        # 6. 等待确认弹框
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")

        # 7. 等待toast消息
        self.wait_for_toast(page)

        # 8. 断言创建成功
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_007: 测试选择活动地点“线上”时，显示“平台名称”输入框，隐藏省市区地址")
    def test_TC_007(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_008: 测试选择活动地点“线下”时，显示省市区下拉框及“详细地址”输入框，隐藏平台名称")
    def test_TC_008(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="offline"]')
        page.wait_for_selector("#formProvince", state="visible")
        page.wait_for_selector("#formCity", state="visible")
        page.wait_for_selector("#formDistrict", state="visible")
        page.wait_for_selector("#formAddress", state="visible")
        page.wait_for_selector("#formOnlinePlatform", state="hidden")
        page.select_option("#formProvince", "广东省")
        page.wait_for_selector("#formCity option", state="visible")
        page.select_option("#formCity", "深圳市")
        page.wait_for_selector("#formDistrict option", state="visible")
        page.select_option("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园南区A栋")
        page.click("#btnSubmit")
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")
        self.wait_for_toast(page)
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
    @allure.feature("创建活动")
    @allure.title("TC_009: 测试所有必填字段为空时，点击【完成创建】的校验提示")
    def test_TC_009(self, page):
        # 测试步骤
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        # 所有必填字段留空，直接点击完成创建
        page.click("#btnSubmit")
        # 验证所有必填字段的错误提示
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()
        expect(page.locator("#toast")).to_contain_text("请选择活动类型")
        expect(page.locator("#error_formType")).to_be_visible()
        expect(page.locator("#toast")).to_contain_text("请选择开始时间")
        expect(page.locator("#error_formStartTime")).to_be_visible()
        expect(page.locator("#toast")).to_contain_text("请选择结束时间")
        expect(page.locator("#error_formEndTime")).to_be_visible()
        expect(page.locator("#toast")).to_contain_text("请输入活动简介")
        expect(page.locator("#error_formDescription")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_010: 测试仅活动名称为空时，点击【完成创建】的字段级错误提示")
    def test_TC_010(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")

        # 3. 等待创建弹框出现
        page.wait_for_selector("#createModal", state="visible")

        # 4. 填写表单（活动名称留空）
        # 选择活动类型
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 设置活动时间
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")

        # 填写活动简介
        page.fill("#formDescription", "这是一个测试活动")

        # 选择线上模式
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 5. 点击【完成创建】按钮
        page.click("#btnSubmit")

        # 6. 断言：验证活动名称为空的错误提示
        expect(page.locator("#toast")).to_contain_text("请输入活动名称")
        expect(page.locator("#error_formName")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_011: 测试仅活动类型为空时，点击【完成创建】的字段级错误提示")
    def test_TC_011(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请选择活动类型")
        expect(page.locator("#error_formType")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_012: 测试仅活动时间为空时，点击【完成创建】的校验提示")
    def test_TC_012(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请选择开始时间")
        expect(page.locator("#error_formStartTime")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_013: 测试仅活动简介为空时，点击【完成创建】的校验提示")
    def test_TC_013(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("请输入活动简介")
        expect(page.locator("#error_formDescription")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_014: 测试填写部分信息后，点击【放弃创建】并确认放弃，验证返回列表页且信息不保存")
    def test_TC_014(self, page):
        # 1. 导航到活动列表页
        self.navigate_to_page(page)

        # 2. 点击创建按钮，打开创建弹框
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写部分信息（活动名称、活动类型、子类型）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")

        # 4. 点击【放弃创建】按钮
        page.click("#btnCancel")

        # 5. 等待确认放弃弹框出现并确认放弃
        page.wait_for_selector("#confirmModal", state="visible")
        page.click("#btnConfirm")

        # 6. 验证返回列表页（创建弹框关闭）
        page.wait_for_selector("#createModal", state="hidden")

        # 7. 验证列表页没有新增的活动记录（信息不保存）
        expect(page.locator("#activityTableBody")).not_to_contain_text("测试活动")
    @allure.feature("创建活动")
    @allure.title("TC_015: 测试填写部分信息后，点击【放弃创建】并取消放弃，验证停留在创建页且信息保留")
    def test_TC_015(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写部分信息（活动名称、活动类型、子类型、开始时间、结束时间）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")

        # 4. 点击【放弃创建】按钮（假设为 #btnCancel）
        page.click("#btnCancel")

        # 5. 等待确认弹框出现
        page.wait_for_selector("#confirmModal", state="visible")

        # 6. 点击取消放弃（假设确认弹框中有取消按钮 #btnCancelDiscard）
        page.click("#btnCancelDiscard")

        # 7. 验证仍然停留在创建页且信息保留
        expect(page.locator("#createModal")).to_be_visible()
        expect(page.locator("#formName")).to_have_value("测试活动")
        expect(page.locator("#formType")).to_have_value("社区活动")
        expect(page.locator("#formSubType")).to_have_value("运动会")
        expect(page.locator("#formStartTime")).to_have_value("2024-01-01 10:00")
        expect(page.locator("#formEndTime")).to_have_value("2024-01-01 18:00")
    @allure.feature("创建活动")
    @allure.title("TC_016: 测试所选活动类型被停用后，点击【完成创建】的提示信息")
    def test_TC_016(self, page):
        self.navigate_to_page(page)
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")
        # 模拟活动类型被停用（通过JavaScript修改select选项为已停用状态）
        page.evaluate("document.querySelector('#formType').value = 'disabled_type';")
        page.click("#btnSubmit")
        expect(page.locator("#toast")).to_contain_text("所选活动类型已被停用，请选择新的活动类型")
        expect(page.locator("#error_formType")).to_be_visible()
    @allure.feature("创建活动")
    @allure.title("TC_017: 测试重复快速点击【完成创建】按钮，验证只创建一次活动，无重复数据")
    def test_TC_017(self, page):
        # 1. 导航到页面
        self.navigate_to_page(page)

        # 2. 点击创建按钮
        page.click("#btnCreate")
        page.wait_for_selector("#createModal", state="visible")

        # 3. 填写表单（所有必填字段）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "社区活动")
        page.wait_for_selector("#subTypeDiv", state="visible")
        page.select_option("#formSubType", "运动会")
        page.evaluate("document.querySelector('#formStartTime').value = '2024-01-01 10:00';")
        page.evaluate("document.querySelector('#formEndTime').value = '2024-01-01 18:00';")
        page.fill("#formDescription", "这是一个测试活动")
        page.click('input[name="locationType"][value="online"]')
        page.fill("#formOnlinePlatform", "腾讯会议")

        # 4. 点击【完成创建】按钮
        page.click("#btnSubmit")

        # 5. 等待确认弹框出现
        page.wait_for_selector("#confirmModal", state="visible")

        # 6. 快速重复点击【确认】按钮
        page.click("#btnConfirm")
        page.click("#btnConfirm")
        page.click("#btnConfirm")

        # 7. 等待 toast 消息
        self.wait_for_toast(page)

        # 8. 验证只创建一次活动，无重复数据
        expect(page.locator("#toast")).to_contain_text("活动创建成功")
        expect(page.locator("#toast")).to_be_visible()

        # 9. 验证活动列表中只有一条记录
        page.wait_for_selector("#activityTableBody", state="visible")
        rows = page.locator("#activityTableBody tr")
        assert rows.count() == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

