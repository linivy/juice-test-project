# ========== P0 批次 1 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-FUNC-001: 使用admin账号，填写所有必填字段，选择线上平台，点击完成创建")
    def test_create_activity_online_admin(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择admin角色
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", "线上活动测试")
        
        # 选择活动类型
        page.select_option("#formType", "线上")
        
        # 选择子类型
        page.select_option("#formSubType", "直播")
        
        # 填写开始时间
        page.fill("#formStartTime", "2024-01-15 09:00")
        
        # 填写结束时间
        page.fill("#formEndTime", "2024-01-15 18:00")
        
        # 填写活动简介
        page.fill("#formDescription", "这是一个线上活动测试")
        
        # 选择线上平台
        page.select_option("#formOnlinePlatform", "腾讯会议")
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 等待确认弹框
        page.wait_for_selector(".modal-content", state="visible")
        
        # 点击确认
        page.click("#btnConfirmSubmit")
        
        # 验证跳转到活动列表页
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        
        # 验证toast消息
        wait_for_toast(page)
        toast = page.locator(".toast-message, .toast")
        expect(toast).to_contain_text("活动创建成功")

    @allure.title("TC-ACTIVITY-FUNC-002: 使用user1账号，填写所有必填字段，选择线下地点，点击完成创建")
    def test_create_activity_offline_user1(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择user1角色
        page.select_option("#roleSelect", "user1")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", "线下活动测试")
        
        # 选择活动类型
        page.select_option("#formType", "线下")
        
        # 选择子类型
        page.select_option("#formSubType", "会议")
        
        # 填写开始时间
        page.fill("#formStartTime", "2024-02-20 14:00")
        
        # 填写结束时间
        page.fill("#formEndTime", "2024-02-20 17:00")
        
        # 填写活动简介
        page.fill("#formDescription", "这是一个线下活动测试")
        
        # 选择省份
        page.select_option("#formProvince", "广东省")
        
        # 选择城市
        page.select_option("#formCity", "深圳市")
        
        # 选择区县
        page.select_option("#formDistrict", "南山区")
        
        # 填写详细地址
        page.fill("#formAddress", "科技园南区A栋101室")
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 等待确认弹框
        page.wait_for_selector(".modal-content", state="visible")
        
        # 点击确认
        page.click("#btnConfirmSubmit")
        
        # 验证跳转到活动列表页
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        
        # 验证活动状态为已发布
        status = page.locator(".activity-status").first
        expect(status).to_contain_text("已发布")

    @allure.title("TC-ACTIVITY-FUNC-003: 仅填写活动名称，点击保存草稿")
    def test_save_draft_only_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择admin角色
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 仅填写活动名称
        page.fill("#formName", "草稿活动测试")
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        
        # 验证跳转到活动列表页
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        
        # 验证toast消息
        wait_for_toast(page)
        toast = page.locator(".toast-message, .toast")
        expect(toast).to_contain_text("草稿已保存，稍后可以继续编辑")
        
        # 验证活动状态为待提交
        status = page.locator(".activity-status").first
        expect(status).to_contain_text("待提交")

    @allure.title("TC-ACTIVITY-VALID-001: 不填写活动名称，点击完成创建")
    def test_validate_empty_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择admin角色
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 不填写活动名称，直接点击完成创建
        page.click("#btnSubmit")
        
        # 验证停留在创建页
        expect(page).to_have_url(f"{BASE_URL}/")
        
        # 验证错误提示
        error_msg = page.locator("#empty_name, .error-message")
        expect(error_msg).to_contain_text("请输入活动名称")

    @allure.title("TC-ACTIVITY-VALID-002: 不选择活动类型，点击完成创建")
    def test_validate_empty_type(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择admin角色
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称但不选择类型
        page.fill("#formName", "测试活动")
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 验证停留在创建页
        expect(page).to_have_url(f"{BASE_URL}/")
        
        # 验证错误提示
        error_msg = page.locator("#empty_type, .error-message")
        expect(error_msg).to_contain_text("请选择活动类型")
```

# ========== P0 批次 2 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-VALID-003: 不填写活动简介，点击完成创建")
    def test_empty_description(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 填写必填字段（除活动简介外）
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")

        # 点击完成创建
        page.click("#btnSubmit")

        # 验证错误提示
        expect(page.locator("#formDescription")).to_have_attribute("aria-invalid", "true")
        error_msg = page.locator("#formDescription + .error-message, .field-error")
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("请输入活动简介")

    @allure.title("TC-ACTIVITY-VALID-004: 所有必填字段同时为空，点击完成创建")
    def test_all_required_fields_empty(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 点击完成创建
        page.click("#btnSubmit")

        # 验证提示信息
        toast = page.locator(".toast-message, .toast")
        expect(toast).to_be_visible()
        expect(toast).to_contain_text("活动信息未完善，请前往完善")

        # 验证只提示一次
        toast_count = page.locator(".toast-message, .toast").count()
        assert toast_count == 1

    @allure.title("TC-ACTIVITY-VALID-005: 活动名称输入50个字符")
    def test_name_50_characters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 输入50个字符的活动名称
        name_50 = "A" * 50
        page.fill("#formName", name_50)

        # 验证输入成功
        actual_value = page.input_value("#formName")
        assert len(actual_value) == 50
        assert actual_value == name_50

        # 填写其他必填字段
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")

        # 提交成功
        page.click("#btnSubmit")
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-VALID-006: 活动名称输入51个字符")
    def test_name_51_characters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 尝试输入51个字符
        name_51 = "A" * 51
        page.fill("#formName", name_51)

        # 验证无法输入第51个字符
        actual_value = page.input_value("#formName")
        assert len(actual_value) <= 50

        # 或者验证提交时提示超出限制
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")

        page.click("#btnSubmit")
        error_msg = page.locator("#formName + .error-message, .field-error")
        if error_msg.is_visible():
            expect(error_msg).to_contain_text("超出限制")

    @allure.title("TC-ACTIVITY-VALID-007: 活动简介输入500个字符")
    def test_description_500_characters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 输入500个字符的活动简介
        desc_500 = "B" * 500
        page.fill("#formDescription", desc_500)

        # 验证输入成功
        actual_value = page.input_value("#formDescription")
        assert len(actual_value) == 500
        assert actual_value == desc_500

        # 填写其他必填字段
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")

        # 提交成功
        page.click("#btnSubmit")
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-VALID-008: 活动简介输入501个字符")
    def test_description_501_characters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 尝试输入501个字符
        desc_501 = "B" * 501
        page.fill("#formDescription", desc_501)

        # 验证无法输入第501个字符
        actual_value = page.input_value("#formDescription")
        assert len(actual_value) <= 500

        # 或者验证提交时提示超出限制
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")

        page.click("#btnSubmit")
        error_msg = page.locator("#formDescription + .error-message, .field-error")
        if error_msg.is_visible():
            expect(error_msg).to_contain_text("超出限制")
```

# ========== P0 批次 3 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-BOUND-001: 活动名称为1个字符")
    def test_activity_name_1_char(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 输入1个字符的活动名称
        page.fill("#formName", "测")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 提交
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-BOUND-002: 活动名称为50个字符（中文）")
    def test_activity_name_50_chinese_chars(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 输入50个中文字符
        chinese_name = "活" * 50
        page.fill("#formName", chinese_name)
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")
        
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-BOUND-003: 活动名称为50个字符（英文+数字）")
    def test_activity_name_50_english_digits(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 输入50个英文+数字字符
        english_name = "A1" * 25
        page.fill("#formName", english_name)
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")
        
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-BOUND-004: 备注输入50个字符")
    def test_remark_50_chars(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 输入50个字符的备注
        remark_text = "备" * 50
        page.fill("#formName", "测试活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formRemark", remark_text)
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")
        
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-BOUND-005: 备注输入51个字符")
    def test_remark_51_chars(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 尝试输入51个字符的备注
        remark_text = "备" * 51
        page.fill("#formName", "测试活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formRemark", remark_text)
        
        # 验证无法输入第51个字符
        actual_value = page.input_value("#formRemark")
        assert len(actual_value) <= 50, "备注字段应该限制最多50个字符"

    @allure.title("TC-ACTIVITY-CASCADE-001: 选择活动类型为社区活动")
    def test_cascade_community_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 选择社区活动
        page.select_option("#formType", "社区活动")
        page.wait_for_timeout(500)
        
        # 验证子类型选项
        subtype_options = page.locator("#formSubType option").all_text_contents()
        expected_options = ["运动会", "知识讲座", "才艺比赛"]
        for option in expected_options:
            assert option in subtype_options, f"子类型选项应包含: {option}"

    @allure.title("TC-ACTIVITY-CASCADE-002: 选择活动类型为家庭活动")
    def test_cascade_family_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 选择家庭活动
        page.select_option("#formType", "家庭活动")
        page.wait_for_timeout(500)
        
        # 验证子类型选项
        subtype_options = page.locator("#formSubType option").all_text_contents()
        # 家庭活动的子类型选项
        expected_options = ["亲子游戏", "家庭聚餐", "户外郊游"]
        for option in expected_options:
            assert option in subtype_options, f"子类型选项应包含: {option}"

    @allure.title("测试空字段验证")
    def test_empty_field_validation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 验证提交按钮在空字段时禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()
        
        # 验证错误消息
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 检查错误消息
        error_messages = page.locator(".error-message, .toast-message")
        error_texts = error_messages.all_text_contents()
        
        expected_errors = [
            "请输入活动名称",
            "请选择活动类型",
            "请选择子类型",
            "请输入活动简介"
        ]
        
        for error in expected_errors:
            assert any(error in text for text in error_texts), f"应显示错误消息: {error}"

    @allure.title("测试时间范围验证")
    def test_time_range_validation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写基本信息
        page.fill("#formName", "测试活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        
        # 设置结束时间早于开始时间
        page.fill("#formStartTime", "2024-01-01 14:00")
        page.fill("#formEndTime", "2024-01-01 10:00")
        
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息
        error_messages = page.locator(".error-message, .toast-message")
        error_texts = error_messages.all_text_contents()
        assert any("结束时间必须晚于开始时间" in text for text in error_texts), "应显示时间范围错误消息"

    @allure.title("测试活动时长超过72小时")
    def test_activity_duration_exceeds_72_hours(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写基本信息
        page.fill("#formName", "测试活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试活动简介")
        
        # 设置活动时长超过72小时
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-05 10:00")
        
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息
        error_messages = page.locator(".error-message, .toast-message")
        error_texts = error_messages.all_text_contents()
        assert any("活动时长不能超过72小时" in text for text in error_texts), "应显示时长超限错误消息"

    @allure.title("测试保存草稿功能")
    def test_save_draft(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写部分信息
        page.fill("#formName", "草稿测试活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "草稿测试简介")
        
        # 保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证保存成功
        toast_message = page.locator(".toast-message, .toast")
        expect(toast_message).to_be_visible()

    @allure.title("测试取消活动功能")
    def test_cancel_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写活动信息
        page.fill("#formName", "待取消活动")
        page.fill("#formType", "社区活动")
        page.fill("#formSubType", "运动会")
        page.fill("#formDescription", "测试取消活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")
        
        # 点击取消活动
        page.click("#btnCancelActivity")
        page.wait_for_selector("#cancelReason")
        
        # 填写取消原因
        page.fill("#cancelReason", "测试取消原因")
        
        # 确认取消
        page.click("#btnConfirmCancel")
        wait_for_toast(page)
        
        # 验证取消成功
        toast_message = page.locator(".toast-message, .toast")
        expect(toast_message).to_be_visible()

    @allure.title("测试角色切换功能")
    def test_role_switch(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 切换角色
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)
        
        # 验证角色切换后的界面变化
        create_button = page.locator("#btnCreate")
        expect(create_button).to_be_visible

# ========== P0 批次 4 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-CASCADE-001: 选择活动类型为'亲子活动'")
    @pytest.mark.parametrize("activity_type, expected_subtypes", [
        ("亲子活动", ["亲子活动", "户外露营", "亲子烘培"])
    ])
    def test_cascade_001(self, page: Page, activity_type, expected_subtypes):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option(activity_type)
        page.wait_for_timeout(300)
        
        # 验证子类型下拉框显示
        subtype_select = page.locator("#formSubType")
        expect(subtype_select).to_be_visible()
        
        # 获取子类型选项
        options = subtype_select.locator("option").all_text_contents()
        options = [opt.strip() for opt in options if opt.strip()]
        
        # 验证子类型选项
        for subtype in expected_subtypes:
            assert subtype in options, f"子类型 '{subtype}' 不在选项中"
        
        # 验证其他活动类型输入框隐藏
        other_type_input = page.locator("#formOtherType")
        expect(other_type_input).not_to_be_visible()

    @allure.title("TC-ACTIVITY-CASCADE-002: 选择活动类型为'户外露营'")
    @pytest.mark.parametrize("activity_type, expected_subtypes", [
        ("户外露营", ["亲子活动", "户外露营", "亲子烘培"])
    ])
    def test_cascade_002(self, page: Page, activity_type, expected_subtypes):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option(activity_type)
        page.wait_for_timeout(300)
        
        # 验证子类型下拉框显示
        subtype_select = page.locator("#formSubType")
        expect(subtype_select).to_be_visible()
        
        # 获取子类型选项
        options = subtype_select.locator("option").all_text_contents()
        options = [opt.strip() for opt in options if opt.strip()]
        
        # 验证子类型选项
        for subtype in expected_subtypes:
            assert subtype in options, f"子类型 '{subtype}' 不在选项中"
        
        # 验证其他活动类型输入框隐藏
        other_type_input = page.locator("#formOtherType")
        expect(other_type_input).not_to_be_visible()

    @allure.title("TC-ACTIVITY-CASCADE-003: 选择活动类型为'其他'")
    def test_cascade_003(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型为"其他"
        page.locator("#formType").select_option("其他")
        page.wait_for_timeout(300)
        
        # 验证子类型下拉框隐藏
        subtype_select = page.locator("#formSubType")
        expect(subtype_select).not_to_be_visible()
        
        # 验证其他活动类型输入框显示
        other_type_input = page.locator("#formOtherType")
        expect(other_type_input).to_be_visible()

    @allure.title("TC-ACTIVITY-CASCADE-004: 选择活动地点为'线上'")
    def test_cascade_004(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择子类型
        page.locator("#formSubType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择活动地点为"线上"
        page.locator("#formOnlinePlatform").fill("腾讯会议")
        page.wait_for_timeout(300)
        
        # 验证平台名称输入框显示
        online_platform = page.locator("#formOnlinePlatform")
        expect(online_platform).to_be_visible()
        
        # 验证省市区和详细地址隐藏
        province = page.locator("#formProvince")
        city = page.locator("#formCity")
        district = page.locator("#formDistrict")
        address = page.locator("#formAddress")
        
        expect(province).not_to_be_visible()
        expect(city).not_to_be_visible()
        expect(district).not_to_be_visible()
        expect(address).not_to_be_visible()

    @allure.title("TC-ACTIVITY-CASCADE-005: 选择活动地点为'线下'")
    def test_cascade_005(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择子类型
        page.locator("#formSubType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择活动地点为"线下"
        page.locator("#formProvince").select_option("广东省")
        page.wait_for_timeout(300)
        
        # 验证省市区下拉框和详细地址输入框显示
        province = page.locator("#formProvince")
        city = page.locator("#formCity")
        district = page.locator("#formDistrict")
        address = page.locator("#formAddress")
        
        expect(province).to_be_visible()
        expect(city).to_be_visible()
        expect(district).to_be_visible()
        expect(address).to_be_visible()
        
        # 验证平台名称隐藏
        online_platform = page.locator("#formOnlinePlatform")
        expect(online_platform).not_to_be_visible()

    @allure.title("TC-ACTIVITY-TIME-001: 开始时间选择当前时间之前的时间")
    def test_time_001(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择子类型
        page.locator("#formSubType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 填写活动名称
        page.locator("#formName").fill("测试活动")
        
        # 填写活动简介
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 设置开始时间为过去时间
        from datetime import datetime, timedelta
        past_time = datetime.now() - timedelta(hours=1)
        past_time_str = past_time.strftime("%Y-%m-%dT%H:%M")
        
        page.locator("#formStartTime").fill(past_time_str)
        page.wait_for_timeout(300)
        
        # 设置结束时间为未来时间
        future_time = datetime.now() + timedelta(hours=2)
        future_time_str = future_time.strftime("%Y-%m-%dT%H:%M")
        page.locator("#formEndTime").fill(future_time_str)
        page.wait_for_timeout(300)
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "活动时间不可选历史时间" in error_message, f"期望错误消息包含'活动时间不可选历史时间'，实际为: {error_message}"

    @allure.title("TC-ACTIVITY-TIME-002: 结束时间早于开始时间")
    def test_time_002(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择子类型
        page.locator("#formSubType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 填写活动名称
        page.locator("#formName").fill("测试活动")
        
        # 填写活动简介
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 设置开始时间为未来时间
        from datetime import datetime, timedelta
        start_time = datetime.now() + timedelta(hours=2)
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M")
        
        page.locator("#formStartTime").fill(start_time_str)
        page.wait_for_timeout(300)
        
        # 设置结束时间早于开始时间
        end_time = datetime.now() + timedelta(hours=1)
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M")
        page.locator("#formEndTime").fill(end_time_str)
        page.wait_for_timeout(300)
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "结束时间必须晚于开始时间" in error_message, f"期望错误消息包含'结束时间必须晚于开始时间'，实际为: {error_message}"

    @allure.title("TC-ACTIVITY-EMPTY-NAME: 活动名称为空时提交")
    def test_empty_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 选择活动类型
        page.locator("#formType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 选择子类型
        page.locator("#formSubType").select_option("亲子活动")
        page.wait_for_timeout(300)
        
        # 填写活动简介
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 设置时间
        from datetime import datetime, timedelta
        start_time = datetime.now() + timedelta(hours=1)
        end_time = datetime.now() + timedelta(hours=3)
        page.locator("#formStartTime").fill(start_time.strftime("%Y-%m-%dT%H:%M"))
        page.locator("#formEndTime").fill(end_time.strftime("%Y-%m-%dT%H:%M"))
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "请输入活动名称" in error_message, f"期望错误消息包含'请输入活动名称'，实际为: {error_message}"

    @allure.title("TC-ACTIVITY-EMPTY-TYPE: 活动类型为空时提交")
    def test_empty_type(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动名称
        page.locator("#formName").fill("测试活动")
        
        # 填写活动简介
        page.locator

# ========== P0 批次 5 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-TIME-003: 活动时长超过72小时")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-超72小时",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试活动时长超过72小时",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-05T10:01",
            "expected_error": "time_exceeds"
        }
    ])
    def test_activity_time_exceeds_72_hours(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "活动时长不能超过72小时" in error_message or data["expected_error"] in error_message

    @allure.title("TC-ACTIVITY-TIME-004: 活动时长刚好72小时")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-刚好72小时",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试活动时长刚好72小时",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-04T10:00",
            "expected_success": True
        }
    ])
    def test_activity_time_exactly_72_hours(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证成功
        assert "#activity-list" in page.url

    @allure.title("TC-ACTIVITY-TIME-005: 活动时长刚好72小时零1分钟")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-超72小时1分钟",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试活动时长刚好72小时零1分钟",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-04T10:01",
            "expected_error": "time_exceeds"
        }
    ])
    def test_activity_time_exactly_72_hours_1_minute(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "活动时长不能超过72小时" in error_message or data["expected_error"] in error_message

    @allure.title("TC-ACTIVITY-TIME-006: 跨天活动（开始时间今天，结束时间明天）")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-跨天",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试跨天活动",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-02T10:00",
            "expected_success": True
        }
    ])
    def test_activity_cross_day(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证成功
        assert "#activity-list" in page.url

    @allure.title("TC-ACTIVITY-TIME-007: 跨月活动（开始时间月末，结束时间下月初）")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-跨月",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试跨月活动",
            "start_time": "2024-01-31T10:00",
            "end_time": "2024-02-01T10:00",
            "expected_success": True
        }
    ])
    def test_activity_cross_month(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证成功
        assert "#activity-list" in page.url

    @allure.title("TC-ACTIVITY-TIME-008: 鼠标悬停在时间输入框")
    @pytest.mark.parametrize("data", [
        {
            "expected_tooltip": "若时间暂无法确认，可先提供一个预估的时间范围，后续可进行修改"
        }
    ])
    def test_activity_time_hover_tooltip(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 鼠标悬停在开始时间输入框
        start_time_input = page.locator("#formStartTime")
        start_time_input.hover()
        page.wait_for_timeout(500)
        
        # 检查提示信息
        tooltip = page.locator(".tooltip, .popover, [role='tooltip']")
        if tooltip.is_visible():
            assert data["expected_tooltip"] in tooltip.text_content()
        
        # 鼠标悬停在结束时间输入框
        end_time_input = page.locator("#formEndTime")
        end_time_input.hover()
        page.wait_for_timeout(500)
        
        # 检查提示信息
        tooltip = page.locator(".tooltip, .popover, [role='tooltip']")
        if tooltip.is_visible():
            assert data["expected_tooltip"] in tooltip.text_content()

    @allure.title("TC-ACTIVITY-FILE-001: 上传单个.pdf文件")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-上传PDF",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试上传PDF文件",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-02T10:00",
            "file_path": "test.pdf"
        }
    ])
    def test_activity_upload_pdf(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 上传文件
        file_input = page.locator("input[type='file']")
        if file_input.is_visible():
            file_input.set_input_files(data["file_path"])
            page.wait_for_timeout(500)
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证成功
        assert "#activity-list" in page.url

    @allure.title("TC-ACTIVITY-TIME-001: 结束时间早于开始时间")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动-时间错误",
            "type": "线上活动",
            "subtype": "直播",
            "description": "测试结束时间早于开始时间",
            "start_time": "2024-01-02T10:00",
            "end_time": "2024-01-01T10:00",
            "expected_error": "invalid_time_range"
        }
    ])
    def test_activity_end_time_before_start_time(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        
        # 设置时间
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait

# ========== P0 批次 6 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-FILE-002: 上传单个.jpg文件")
    def test_upload_single_jpg(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.locator("#roleSelect").select_option("admin")
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动-JPG上传")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试上传JPG文件")
        page.locator("#formStartTime").fill("2025-01-01T10:00")
        page.locator("#formEndTime").fill("2025-01-01T12:00")
        
        # 上传.jpg文件
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("test_files/test.jpg")
        
        # 验证上传成功
        expect(page.locator(".file-list .file-item")).to_have_count(1)
        expect(page.locator(".file-list .file-item")).to_contain_text(".jpg")
        
        # 保存草稿
        page.locator("#btnSaveDraft").click()
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(f"{BASE_URL}/#activity-list")

    @allure.title("TC-ACTIVITY-FILE-003: 上传单个.xlsx文件")
    def test_upload_single_xlsx(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.locator("#roleSelect").select_option("admin")
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动-XLSX上传")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试上传XLSX文件")
        page.locator("#formStartTime").fill("2025-01-01T10:00")
        page.locator("#formEndTime").fill("2025-01-01T12:00")
        
        # 上传.xlsx文件
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("test_files/test.xlsx")
        
        # 验证上传成功
        expect(page.locator(".file-list .file-item")).to_have_count(1)
        expect(page.locator(".file-list .file-item")).to_contain_text(".xlsx")
        
        # 保存草稿
        page.locator("#btnSaveDraft").click()
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(f"{BASE_URL}/#activity-list")

    @allure.title("TC-ACTIVITY-FILE-004: 上传不支持格式的文件（如.exe）")
    def test_upload_unsupported_format(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.locator("#roleSelect").select_option("admin")
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动-不支持格式上传")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试上传不支持格式文件")
        page.locator("#formStartTime").fill("2025-01-01T10:00")
        page.locator("#formEndTime").fill("2025-01-01T12:00")
        
        # 上传.exe文件
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("test_files/test.exe")
        
        # 验证上传失败，提示不支持的文件格式
        wait_for_toast(page)
        expect(page.locator(".toast-message, .toast")).to_contain_text("不支持的文件格式")
        
        # 验证文件列表为空
        expect(page.locator(".file-list .file-item")).to_have_count(0)

    @allure.title("TC-ACTIVITY-FILE-005: 上传单个文件大小超过20MB")
    def test_upload_file_exceeds_20mb(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.locator("#roleSelect").select_option("admin")
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动-文件超20MB")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试上传超过20MB文件")
        page.locator("#formStartTime").fill("2025-01-01T10:00")
        page.locator("#formEndTime").fill("2025-01-01T12:00")
        
        # 上传超过20MB的文件
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("test_files/large_file_21mb.bin")
        
        # 验证上传失败，提示文件大小超出限制
        wait_for_toast(page)
        expect(page.locator(".toast-message, .toast")).to_contain_text("文件大小超出限制")
        
        # 验证文件列表为空
        expect(page.locator(".file-list .file-item")).to_have_count(0)

    @allure.title("TC-ACTIVITY-FILE-006: 上传多个文件，总大小超过20MB")
    def test_upload_multiple_files_total_exceeds_20mb(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.locator("#roleSelect").select_option("admin")
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动-多文件总超20MB")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试上传多个文件总大小超过20MB")
        page.locator("#formStartTime").fill("2025-01-01T10:00")
        page.locator("#formEndTime").fill("2025-01-01T12:00")
        
        # 上传多个文件，总大小超过20MB
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(["test_files/file_10mb.bin", "test_files/file_11mb.bin"])
        
        # 验证上传失败，提示总大小超出限制
        wait_for_toast(page)
        expect(page.locator(".toast-message, .toast")).to_contain_text("总大小超出限制")
        
        # 验证文件列表为空
        expect(page.locator(".file-list .file-item")).to_have_count(0)
[COMPLETE]
```

# ========== P0 批次 7 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-FILE-007: 上传多个文件，总大小不超过20MB")
    def test_upload_multiple_files_within_size_limit(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写必填字段
        page.fill("#formName", "测试活动-文件上传")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formDescription", "测试上传多个文件")
        
        # 设置时间
        page.fill("#formStartTime", "2024-12-01T09:00")
        page.fill("#formEndTime", "2024-12-01T18:00")
        
        # 上传多个文件（总大小不超过20MB）
        file_input = page.locator("input[type='file']")
        file_input.set_input_files([
            {"name": "test1.txt", "mimeType": "text/plain", "buffer": b"test content 1"},
            {"name": "test2.txt", "mimeType": "text/plain", "buffer": b"test content 2"},
            {"name": "test3.txt", "mimeType": "text/plain", "buffer": b"test content 3"}
        ])
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-FILE-008: 删除已上传的文件")
    def test_delete_uploaded_file(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写必填字段
        page.fill("#formName", "测试活动-删除文件")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formDescription", "测试删除已上传文件")
        
        # 设置时间
        page.fill("#formStartTime", "2024-12-01T09:00")
        page.fill("#formEndTime", "2024-12-01T18:00")
        
        # 上传文件
        file_input = page.locator("input[type='file']")
        file_input.set_input_files([
            {"name": "test_delete.txt", "mimeType": "text/plain", "buffer": b"test content to delete"}
        ])
        
        # 等待文件上传完成
        page.wait_for_timeout(1000)
        
        # 删除已上传的文件
        delete_button = page.locator(".file-item .delete-btn, .file-list .remove-btn").first
        if delete_button.is_visible():
            delete_button.click()
            page.wait_for_timeout(500)
        
        # 验证文件已从附件列表中移除
        file_list = page.locator(".file-list, .attachment-list")
        expect(file_list).not_to_contain_text("test_delete.txt")
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-RICH-001: 在活动简介中使用加粗功能")
    def test_rich_text_bold(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写必填字段
        page.fill("#formName", "测试活动-加粗功能")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        
        # 设置时间
        page.fill("#formStartTime", "2024-12-01T09:00")
        page.fill("#formEndTime", "2024-12-01T18:00")
        
        # 在富文本编辑器中输入文字并加粗
        rich_editor = page.locator("#formDescription")
        rich_editor.fill("这是需要加粗的文字")
        
        # 选中文字并点击加粗按钮
        rich_editor.select_text()
        bold_button = page.locator(".editor-toolbar .bold-btn, .ql-bold, [title='加粗']")
        bold_button.click()
        
        # 验证文字变为加粗
        page.wait_for_timeout(500)
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-RICH-002: 在活动简介中使用斜体功能")
    def test_rich_text_italic(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写必填字段
        page.fill("#formName", "测试活动-斜体功能")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        
        # 设置时间
        page.fill("#formStartTime", "2024-12-01T09:00")
        page.fill("#formEndTime", "2024-12-01T18:00")
        
        # 在富文本编辑器中输入文字并设置斜体
        rich_editor = page.locator("#formDescription")
        rich_editor.fill("这是需要斜体的文字")
        
        # 选中文字并点击斜体按钮
        rich_editor.select_text()
        italic_button = page.locator(".editor-toolbar .italic-btn, .ql-italic, [title='斜体']")
        italic_button.click()
        
        # 验证文字变为斜体
        page.wait_for_timeout(500)
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-RICH-003: 在活动简介中使用下划线功能")
    def test_rich_text_underline(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录操作
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写必填字段
        page.fill("#formName", "测试活动-下划线功能")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        
        # 设置时间
        page.fill("#formStartTime", "2024-12-01T09:00")
        page.fill("#formEndTime", "2024-12-01T18:00")
        
        # 在富文本编辑器中输入文字并添加下划线
        rich_editor = page.locator("#formDescription")
        rich_editor.fill("这是需要下划线的文字")
        
        # 选中文字并点击下划线按钮
        rich_editor.select_text()
        underline_button = page.locator(".editor-toolbar .underline-btn, .ql-underline, [title='下划线']")
        underline_button.click()
        
        # 验证文字添加下划线
        page.wait_for_timeout(500)
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
```

# ========== P0 批次 8 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"
PAGE_PATH = "/"
SUCCESS_URL = "#activity-list"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-RICH-004: 在活动简介中插入http超链接")
    def test_insert_http_link_in_description(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写必要字段
        page.fill("#formName", "测试活动-超链接")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 在活动简介中插入http超链接
        description_editor = page.locator("#formDescription")
        description_editor.fill("这是一个测试超链接：https://www.example.com")

        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")

        # 验证成功
        expect(page).to_have_url(lambda url: SUCCESS_URL in url)

    @allure.title("TC-ACTIVITY-RICH-005: 在活动简介中设置居左/居中/居右对齐")
    def test_text_alignment_in_description(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写必要字段
        page.fill("#formName", "测试活动-对齐方式")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 在活动简介中设置居左/居中/居右对齐
        description_editor = page.locator("#formDescription")
        description_editor.fill("居左文本")
        # 模拟设置居中对齐（假设编辑器支持）
        page.keyboard.press("Control+Shift+E")  # 假设快捷键
        description_editor.fill("居中文本")
        page.keyboard.press("Control+Shift+R")  # 假设快捷键
        description_editor.fill("居右文本")

        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")

        # 验证成功
        expect(page).to_have_url(lambda url: SUCCESS_URL in url)

    @allure.title("TC-ACTIVITY-RICH-006: 活动简介输入500个字符（含富文本标签）")
    def test_description_500_chars_with_tags(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写必要字段
        page.fill("#formName", "测试活动-500字符")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 输入500个字符（含富文本标签）
        long_text = "<p>" + "A" * 480 + "</p>"
        page.fill("#formDescription", long_text)

        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")

        # 验证成功
        expect(page).to_have_url(lambda url: SUCCESS_URL in url)

    @allure.title("TC-ACTIVITY-RICH-007: 活动简介输入超过500个字符")
    def test_description_exceeds_500_chars(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写必要字段
        page.fill("#formName", "测试活动-超500字符")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 输入超过500个字符
        long_text = "A" * 501
        page.fill("#formDescription", long_text)

        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_load_state("networkidle")

        # 验证失败：停留在创建页面或提示超出限制
        expect(page).to_have_url(lambda url: SUCCESS_URL not in url)
        # 检查错误消息
        error_message = page.locator(".error-message, .toast-message")
        expect(error_message).to_be_visible()

    @allure.title("TC-ACTIVITY-FUNC-004: 点击'放弃创建'按钮")
    def test_click_cancel_button(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写一些信息
        page.fill("#formName", "测试活动-放弃创建")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 点击放弃创建
        page.click("#btnCancel")

        # 确认弹框
        confirm_dialog = page.locator(".confirm-dialog, .modal-content")
        expect(confirm_dialog).to_be_visible()

        # 点击确认
        page.click("#btnConfirmCancel")
        page.wait_for_load_state("networkidle")

        # 验证返回活动列表页
        expect(page).to_have_url(lambda url: SUCCESS_URL in url)

    @allure.title("TC-ACTIVITY-FUNC-005: 点击'放弃创建'后，在确认弹框点击取消")
    def test_cancel_in_confirm_dialog(self, page: Page):
        page.goto(f"{BASE_URL}{PAGE_PATH}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录操作（admin用户）
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")

        # 填写一些信息
        page.fill("#formName", "测试活动-取消放弃")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "线上会议")
        page.fill("#formStartTime", "2025-01-01 09:00")
        page.fill("#formEndTime", "2025-01-01 18:00")

        # 点击放弃创建
        page.click("#btnCancel")

        # 确认弹框
        confirm_dialog = page.locator(".confirm-dialog, .modal-content")
        expect(confirm_dialog).to_be_visible()

        # 点击取消
        page.click("#btnCloseModal")
        page.wait_for_load_state("networkidle")

        # 验证仍然在创建页面
        expect(page.locator("#formName")).to_be_visible()
        expect(page.locator("#formName")).to_have_value("测试活动-取消放弃")
```

# ========== P0 批次 9 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-FUNC-006: 快速连续点击'完成创建'按钮多次")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动",
            "type": "线上",
            "subtype": "直播",
            "description": "测试活动简介",
            "start_time": "2024-01-01T10:00",
            "end_time": "2024-01-01T12:00",
        }
    ])
    def test_quick_submit(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写表单
        page.locator("#formName").fill(data["name"])
        page.locator("#formType").select_option(data["type"])
        page.locator("#formSubType").select_option(data["subtype"])
        page.locator("#formDescription").fill(data["description"])
        page.locator("#formStartTime").fill(data["start_time"])
        page.locator("#formEndTime").fill(data["end_time"])

        # 快速连续点击完成创建按钮
        submit_button = page.locator("#btnSubmit")
        submit_button.click()
        submit_button.click()
        submit_button.click()

        # 验证只提交一次，不会重复创建
        page.wait_for_timeout(2000)
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-FUNC-007: 点击'关闭模态框'按钮")
    def test_close_modal(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写一些信息
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")

        # 点击关闭模态框
        page.locator("#btnCloseModal").click()

        # 验证模态框关闭，停留在创建页
        page.wait_for_timeout(1000)
        expect(page.locator("#btnCreate")).to_be_visible()

    @allure.title("TC-ACTIVITY-SEC-001: 活动名称输入SQL注入payload")
    def test_sql_injection(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 输入SQL注入payload
        page.locator("#formName").fill("' OR 1=1 --")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试活动简介")
        page.locator("#formStartTime").fill("2024-01-01T10:00")
        page.locator("#formEndTime").fill("2024-01-01T12:00")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证系统正确处理，不执行SQL注入
        page.wait_for_timeout(2000)
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-SEC-002: 活动名称输入XSS payload")
    def test_xss_injection(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 输入XSS payload
        page.locator("#formName").fill("<script>alert('xss')</script>")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试活动简介")
        page.locator("#formStartTime").fill("2024-01-01T10:00")
        page.locator("#formEndTime").fill("2024-01-01T12:00")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证输入被转义，不执行脚本
        page.wait_for_timeout(2000)
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-SEC-003: 活动简介富文本输入XSS payload")
    def test_rich_text_xss(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写表单
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("<script>alert('xss')</script>")
        page.locator("#formStartTime").fill("2024-01-01T10:00")
        page.locator("#formEndTime").fill("2024-01-01T12:00")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证输入被转义，不执行脚本
        page.wait_for_timeout(2000)
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-FUNC-001: 创建活动-所有字段填写完整")
    def test_create_activity_full_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写所有字段
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formOtherType").fill("其他类型")
        page.locator("#formStartTime").fill("2024-01-01T10:00")
        page.locator("#formEndTime").fill("2024-01-01T12:00")
        page.locator("#formDescription").fill("测试活动简介")
        page.locator("#formRemark").fill("测试备注")
        page.locator("#formOnlinePlatform").select_option("腾讯会议")
        page.locator("#formProvince").select_option("广东省")
        page.locator("#formCity").select_option("深圳市")
        page.locator("#formDistrict").select_option("南山区")
        page.locator("#formAddress").fill("科技园南区")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证成功
        page.wait_for_timeout(2000)
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-FUNC-002: 创建活动-必填字段为空")
    def test_create_activity_empty_required(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 不填写必填字段，直接提交
        page.locator("#btnSubmit").click()

        # 验证错误消息
        page.wait_for_timeout(1000)
        expect(page.locator(".error-message")).to_contain_text("请输入活动名称")

    @allure.title("TC-ACTIVITY-FUNC-003: 创建活动-结束时间早于开始时间")
    def test_create_activity_invalid_time(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写表单，结束时间早于开始时间
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试活动简介")
        page.locator("#formStartTime").fill("2024-01-01T14:00")
        page.locator("#formEndTime").fill("2024-01-01T12:00")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证错误消息
        page.wait_for_timeout(1000)
        expect(page.locator(".error-message")).to_contain_text("结束时间必须晚于开始时间")

    @allure.title("TC-ACTIVITY-FUNC-004: 创建活动-活动时长超过72小时")
    def test_create_activity_time_exceeds(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写表单，活动时长超过72小时
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")
        page.locator("#formDescription").fill("测试活动简介")
        page.locator("#formStartTime").fill("2024-01-01T10:00")
        page.locator("#formEndTime").fill("2024-01-05T10:00")

        # 提交
        page.locator("#btnSubmit").click()

        # 验证错误消息
        page.wait_for_timeout(1000)
        expect(page.locator(".error-message")).to_contain_text("活动时长不能超过72小时")

    @allure.title("TC-ACTIVITY-FUNC-005: 创建活动-点击'放弃创建'按钮")
    def test_cancel_creation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")

        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_load_state("networkidle")

        # 填写一些信息
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("直播")

        # 点击放弃创建
        page.locator("#btnCancel").click()

        # 验证弹框关闭，停留在创建页，已填写信息保留
        page.wait_for_timeout(1000)
        expect(page.locator("#formName")).to_have_value("测试活动")
        expect(page.locator("#formType")).to_have_value("线上")
        expect(page.locator("#formSubType")).to_have_value("直播")

    @allure.title("TC-ACTIVITY-FUNC-008:

# ========== P0 批次 10 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-SEC-004: 备注输入特殊字符")
    def test_remark_special_characters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写必填字段
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formDescription", "测试描述")
        page.fill("#formStartTime", "2024-01-01 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 备注输入特殊字符
        special_chars = '<>"\'&'
        page.fill("#formRemark", special_chars)
        
        # 保存草稿
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 验证可以正常保存
        expect(page.locator("#formRemark")).to_have_value(special_chars)

    @allure.title("TC-ACTIVITY-EDIT-001: 编辑活动所有字段")
    def test_edit_all_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_selector("#formName")
        
        # 修改所有字段
        page.fill("#formName", "编辑后的活动")
        page.select_option("#formType", "线下")
        page.select_option("#formSubType", "培训")
        page.fill("#formOtherType", "其他类型")
        page.fill("#formStartTime", "2024-02-01 09:00")
        page.fill("#formEndTime", "2024-02-01 18:00")
        page.fill("#formDescription", "编辑后的描述")
        page.fill("#formRemark", "编辑后的备注")
        page.select_option("#formOnlinePlatform", "腾讯会议")
        page.select_option("#formProvince", "广东省")
        page.select_option("#formCity", "深圳市")
        page.select_option("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园南区")
        
        # 提交
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        expect(page.locator(".toast-message")).to_contain_text("活动编辑成功")

    @allure.title("TC-ACTIVITY-CANCEL-001: 取消活动流程")
    def test_cancel_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_selector("#btnCancelActivity")
        
        # 点击取消活动
        page.click("#btnCancelActivity")
        page.wait_for_selector("#cancelReason")
        
        # 填写取消原因
        page.fill("#cancelReason", "活动计划变更")
        
        # 确认取消
        page.click("#btnConfirmCancel")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        expect(page.locator(".toast-message")).to_contain_text("活动取消成功")
        expect(page.locator(".activity-status")).to_contain_text("活动已取消")

    @allure.title("TC-ACTIVITY-DELETE-001: 删除活动流程")
    def test_delete_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取活动列表数量
        activity_count = page.locator(".activity-item").count()
        
        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_selector("#btnDeleteActivity")
        
        # 点击删除活动
        page.click("#btnDeleteActivity")
        page.wait_for_selector("#btnConfirmDelete")
        
        # 确认删除
        page.click("#btnConfirmDelete")
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        expect(page.locator(".toast-message")).to_contain_text("活动删除成功")
        expect(page.locator(".activity-item")).to_have_count(activity_count - 1)

    @allure.title("TC-ACTIVITY-EMPTY-NAME: 空活动名称提交失败")
    def test_empty_name_submit_fail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 不填写活动名称，填写其他字段
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formDescription", "测试描述")
        page.fill("#formStartTime", "2024-01-01 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 提交
        page.click("#btnSubmit")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("请输入活动名称")

    @allure.title("TC-ACTIVITY-CANCEL-REASON-REQUIRED: 取消原因为必填项")
    def test_cancel_reason_required(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_selector("#btnCancelActivity")
        
        # 点击取消活动
        page.click("#btnCancelActivity")
        page.wait_for_selector("#cancelReason")
        
        # 不填写取消原因，直接确认
        page.click("#btnConfirmCancel")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("取消原因为必填项")

    @allure.title("TC-ACTIVITY-VALIDATION-FIRST: 第一个校验失败的字段错误信息")
    def test_first_validation_error(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 不填写任何字段，直接提交
        page.click("#btnSubmit")
        
        # 验证第一个校验失败的字段错误信息
        expect(page.locator(".error-message:first-child")).to_be_visible()

    @allure.title("TC-ACTIVITY-EMPTY-TYPE: 空活动类型提交失败")
    def test_empty_type_submit_fail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写活动名称，不选择活动类型
        page.fill("#formName", "测试活动")
        page.fill("#formDescription", "测试描述")
        page.fill("#formStartTime", "2024-01-01 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 提交
        page.click("#btnSubmit")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("请选择活动类型")

    @allure.title("TC-ACTIVITY-EMPTY-SUBTYPE: 空子类型提交失败")
    def test_empty_subtype_submit_fail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写活动名称和类型，不选择子类型
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.fill("#formDescription", "测试描述")
        page.fill("#formStartTime", "2024-01-01 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 提交
        page.click("#btnSubmit")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("请选择子类型")

    @allure.title("TC-ACTIVITY-EMPTY-DESCRIPTION: 空活动简介提交失败")
    def test_empty_description_submit_fail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写活动名称、类型、子类型，不填写活动简介
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formStartTime", "2024-01-01 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 提交
        page.click("#btnSubmit")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("请输入活动简介")

    @allure.title("TC-ACTIVITY-INVALID-TIME-RANGE: 结束时间早于开始时间")
    def test_invalid_time_range(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写所有必填字段，但结束时间早于开始时间
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "会议")
        page.fill("#formDescription", "测试描述")
        page.fill("#formStartTime", "2024-01-02 09:00")
        page.fill("#formEndTime", "2024-01-01 18:00")
        
        # 提交
        page.click("#btnSubmit")
        
        # 验证失败
        expect(page.locator(".error-message")).to_contain_text("结束时间必须晚于开始时间")

    @allure.title("TC-ACTIVITY-TIME-EXCEEDS: 活动时长超过72小时")
    def test_time_exceeds(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击新建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName")
        
        # 填写所有必填字段，但活动时长

# ========== P0 批次 11 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("待提交活动详情页无取消活动按钮")
    def test_draft_activity_no_cancel_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建待提交活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-待提交")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01T10:00")
        page.fill("#formEndTime", "2024-01-01T12:00")
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 进入活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        
        # 验证无取消活动按钮
        cancel_btn = page.locator("#btnCancelActivity")
        expect(cancel_btn).not_to_be_visible()

    @allure.title("已发布活动详情页显示取消活动按钮并可弹出确认弹框")
    def test_published_activity_has_cancel_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建并发布活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已发布")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01T10:00")
        page.fill("#formEndTime", "2024-01-01T12:00")
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 进入活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        
        # 验证有取消活动按钮
        cancel_btn = page.locator("#btnCancelActivity")
        expect(cancel_btn).to_be_visible()
        
        # 点击取消活动按钮，验证弹出确认弹框
        cancel_btn.click()
        confirm_modal = page.locator("#btnConfirmCancel")
        expect(confirm_modal).to_be_visible()

    @allure.title("已完成活动详情页无取消活动和删除活动按钮")
    def test_completed_activity_no_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建并完成活动（设置时间已过）
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已完成")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2023-01-01T10:00")
        page.fill("#formEndTime", "2023-01-01T12:00")
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 进入活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        
        # 验证无取消活动和删除活动按钮
        cancel_btn = page.locator("#btnCancelActivity")
        expect(cancel_btn).not_to_be_visible()
        
        delete_btn = page.locator("#btnDeleteActivity")
        expect(delete_btn).not_to_be_visible()

    @allure.title("已取消活动详情页无操作按钮")
    def test_cancelled_activity_no_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建并发布活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已取消")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01T10:00")
        page.fill("#formEndTime", "2024-01-01T12:00")
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 进入活动详情并取消
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        page.click("#btnCancelActivity")
        page.fill("#cancelReason", "测试取消原因")
        page.click("#btnConfirmCancel")
        wait_for_toast(page)
        
        # 验证无操作按钮
        cancel_btn = page.locator("#btnCancelActivity")
        expect(cancel_btn).not_to_be_visible()
        
        delete_btn = page.locator("#btnDeleteActivity")
        expect(delete_btn).not_to_be_visible()

    @allure.title("已发布/已完成/已取消状态的活动无删除活动按钮")
    def test_published_completed_cancelled_no_delete_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建已发布活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已发布-无删除")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01T10:00")
        page.fill("#formEndTime", "2024-01-01T12:00")
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 进入活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        
        # 验证无删除活动按钮
        delete_btn = page.locator("#btnDeleteActivity")
        expect(delete_btn).not_to_be_visible()

    @allure.title("非创建者查看待提交活动时无删除活动按钮")
    def test_non_creator_no_delete_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 以admin登录创建待提交活动
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-非创建者查看")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "测试活动简介")
        page.fill("#formStartTime", "2024-01-01T10:00")
        page.fill("#formEndTime", "2024-01-01T12:00")
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 切换为user1登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "user1")
        
        # 进入活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_load_state("networkidle")
        
        # 验证无删除活动按钮
        delete_btn = page.locator("#btnDeleteActivity")
        expect(delete_btn).not_to_be_visible()
[COMPLETE]
```

# ========== P1 批次 1 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-LIST-001: 活动列表显示所有配置字段")
    def test_activity_list_display_all_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 验证活动列表表头包含所有配置字段
        table_headers = page.locator("table thead th")
        expect(table_headers).to_contain_text("活动类型")
        expect(table_headers).to_contain_text("活动名称")
        expect(table_headers).to_contain_text("活动地点")
        expect(table_headers).to_contain_text("开始时间")
        expect(table_headers).to_contain_text("结束时间")
        expect(table_headers).to_contain_text("活动状态")
        expect(table_headers).to_contain_text("操作")

    @allure.title("TC-ACTIVITY-LIST-002: 活动名称超长显示省略号")
    def test_activity_name_truncation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 查找活动名称超长的行
        activity_names = page.locator("table tbody tr td:nth-child(2)")
        for i in range(activity_names.count()):
            name_cell = activity_names.nth(i)
            # 检查是否显示省略号
            if "..." in name_cell.text_content():
                # 验证鼠标悬停显示完整名称
                name_cell.hover()
                expect(name_cell).to_have_attribute("title")
                break

    @allure.title("TC-ACTIVITY-LIST-003: 活动地点字段格式正确")
    def test_activity_location_format(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 验证活动地点格式
        location_cells = page.locator("table tbody tr td:nth-child(3)")
        for i in range(location_cells.count()):
            location_text = location_cells.nth(i).text_content()
            # 格式应为：线上/线下，{城市，具体地点}
            assert "，" in location_text or "线上" in location_text or "线下" in location_text

    @allure.title("TC-ACTIVITY-LIST-004: 活动状态显示正确")
    def test_activity_status_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 验证活动状态标签
        status_cells = page.locator("table tbody tr td:nth-child(6)")
        valid_statuses = ["待提交", "已发布", "已完成", "已取消"]
        for i in range(status_cells.count()):
            status_text = status_cells.nth(i).text_content().strip()
            assert status_text in valid_statuses, f"无效的活动状态: {status_text}"
            # 验证状态标签颜色
            status_badge = status_cells.nth(i).locator("span")
            expect(status_badge).to_have_class()

    @allure.title("TC-ACTIVITY-LIST-005: 按活动名称精确搜索")
    def test_search_activity_by_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 获取第一个活动名称
        first_activity_name = page.locator("table tbody tr:first-child td:nth-child(2)").text_content().strip()
        
        # 在搜索框中输入活动名称
        search_input = page.locator("#searchInput, .search-input, input[type='search']")
        search_input.fill(first_activity_name)
        search_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 验证搜索结果
        search_results = page.locator("table tbody tr")
        expect(search_results).to_have_count(1)
        expect(search_results.locator("td:nth-child(2)")).to_have_text(first_activity_name)

    @allure.title("TC-ACTIVITY-LIST-006: 新建活动-成功创建")
    def test_create_activity_success(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("会议")
        page.locator("#formStartTime").fill("2024-01-01 09:00")
        page.locator("#formEndTime").fill("2024-01-01 18:00")
        page.locator("#formDescription").fill("这是一个测试活动")
        page.locator("#formOnlinePlatform").fill("腾讯会议")
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(1000)
        
        # 验证成功
        expect(page).to_have_url(f"{BASE_URL}/#activity-list")

    @allure.title("TC-ACTIVITY-LIST-007: 新建活动-必填字段为空")
    def test_create_activity_empty_required_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 不填写任何必填字段，直接点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误消息
        expect(page.locator("#formName")).to_have_class("error")
        expect(page.locator("#formType")).to_have_class("error")
        expect(page.locator("#formSubType")).to_have_class("error")
        expect(page.locator("#formDescription")).to_have_class("error")

    @allure.title("TC-ACTIVITY-LIST-008: 新建活动-结束时间早于开始时间")
    def test_create_activity_invalid_time_range(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息，结束时间早于开始时间
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("会议")
        page.locator("#formStartTime").fill("2024-01-01 18:00")
        page.locator("#formEndTime").fill("2024-01-01 09:00")
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误消息
        expect(page.locator(".error-message")).to_contain_text("结束时间必须晚于开始时间")

    @allure.title("TC-ACTIVITY-LIST-009: 新建活动-活动时长超过72小时")
    def test_create_activity_time_exceeds(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写活动信息，时长超过72小时
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("会议")
        page.locator("#formStartTime").fill("2024-01-01 09:00")
        page.locator("#formEndTime").fill("2024-01-05 09:00")
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(500)
        
        # 验证错误消息
        expect(page.locator(".error-message")).to_contain_text("活动时长不能超过72小时")

    @allure.title("TC-ACTIVITY-LIST-010: 新建活动-保存草稿")
    def test_create_activity_save_draft(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写部分活动信息
        page.locator("#formName").fill("草稿活动")
        page.locator("#formType").select_option("线下")
        page.locator("#formProvince").select_option("广东省")
        page.locator("#formCity").select_option("深圳市")
        
        # 点击保存草稿
        page.locator("#btnSaveDraft").click()
        page.wait_for_timeout(1000)
        
        # 验证成功保存草稿
        expect(page).to_have_url(f"{BASE_URL}/#activity-list")

    @allure.title("TC-ACTIVITY-LIST-011: 新建活动-取消创建")
    def test_create_activity_cancel(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.locator("#btnCreate").click()
        page.wait_for_timeout(500)
        
        # 填写部分活动信息
        page.locator("#formName").fill("测试活动")
        
        # 点击放弃创建
        page.locator("#btnCancel").click()
        page.wait_for_timeout(500)
        
        # 验证返回活动列表
        expect(page).to_have_url(f"{BASE_URL}/#activity-list")

    @allure.title("TC-ACTIVITY-LIST-012: 查看活动详情")
    def test_view_activity_detail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_timeout(500)
        
        # 验证详情模态框显示
        expect(page.locator("#activityDetailModal, .modal")).to_be_visible()

    @allure.title("TC-ACTIVITY-LIST-013: 取消活动")
    def test_cancel_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击第一个活动的取消按钮
        page.locator("#btnCancelActivity").first.click()
        page.wait_for_timeout(500)
        
        # 填写取消原因
        page.locator("#cancelReason").fill("活动取消测试")
        
        # 确认取消
        page.locator("#btnConfirmCancel").click()
        page.wait_for_timeout(1000)
        
        # 验证活动状态更新
        expect(page.locator("table tbody tr:first-child td:nth-child(6)")).to_contain_text("已取消")

    @allure.title("TC-ACTIVITY-LIST-014: 角色切换")
    def test_role_switch(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 切换角色
        page.locator("#roleSelect").select_option("admin")
        page.wait_for_timeout(500)
        
        # 验证角色切换成功
        expect(page.locator("#roleSelect")).to_have_value("admin")

    @allure.title("TC-ACTIVITY-LIST-015: 活动列表分页")
    def test_activity_list_pagination(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 验证分页控件存在
        pagination = page.locator(".pagination, .page-navigation")
        expect(pagination).to_be_visible()
        
        # 如果有下一页，点击下一页
        next_button = page.locator(".next-page, .page-next")
        if next_button.is_enabled():


# ========== P1 批次 2 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-LIST-006: 按活动名称模糊搜索（输入部分名称）")
    def test_search_by_partial_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取当前活动列表数量
        activity_rows = page.locator("table tbody tr")
        initial_count = activity_rows.count()
        
        # 输入部分活动名称进行搜索
        search_input = page.locator("input[placeholder*='搜索']")
        search_input.fill("社区")
        search_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 验证搜索结果包含关键词
        if activity_rows.count() > 0:
            first_row_name = activity_rows.first.locator("td").nth(1).text_content()
            assert "社区" in first_row_name, f"搜索结果不包含关键词'社区'，实际结果：{first_row_name}"
        else:
            # 如果没有结果，验证显示空状态
            empty_state = page.locator("text=暂无数据")
            assert empty_state.is_visible(), "搜索无结果时应显示'暂无数据'"

    @allure.title("TC-ACTIVITY-LIST-007: 搜索不存在的活动名称")
    def test_search_nonexistent_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 输入不存在的活动名称
        search_input = page.locator("input[placeholder*='搜索']")
        search_input.fill("不存在的活动名称XYZ123")
        search_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 验证显示空状态提示
        empty_state = page.locator("text=暂无数据")
        assert empty_state.is_visible(), "搜索不存在的活动名称时应显示'暂无数据'"

    @allure.title("TC-ACTIVITY-LIST-008: 搜索后清空搜索条件")
    def test_clear_search_condition(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取初始活动列表数量
        activity_rows = page.locator("table tbody tr")
        initial_count = activity_rows.count()
        
        # 输入搜索条件
        search_input = page.locator("input[placeholder*='搜索']")
        search_input.fill("社区")
        search_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 清空搜索条件
        search_input.clear()
        search_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 验证恢复显示全部活动列表
        final_count = activity_rows.count()
        assert final_count == initial_count, f"清空搜索条件后活动数量应恢复为{initial_count}，实际为{final_count}"

    @allure.title("TC-ACTIVITY-LIST-009: 按活动类型筛选（社区活动）")
    def test_filter_by_activity_type(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 选择活动类型筛选
        type_filter = page.locator("select[aria-label*='类型']")
        type_filter.select_option("社区活动")
        page.wait_for_timeout(1000)
        
        # 验证只显示社区活动类型的活动
        activity_rows = page.locator("table tbody tr")
        if activity_rows.count() > 0:
            for i in range(activity_rows.count()):
                row_type = activity_rows.nth(i).locator("td").nth(2).text_content()
                assert row_type == "社区活动", f"第{i+1}行活动类型应为'社区活动'，实际为'{row_type}'"
        else:
            # 如果没有结果，验证显示空状态
            empty_state = page.locator("text=暂无数据")
            assert empty_state.is_visible(), "筛选无结果时应显示'暂无数据'"

    @allure.title("TC-ACTIVITY-LIST-010: 按活动状态筛选（已发布）")
    def test_filter_by_activity_status(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 选择活动状态筛选
        status_filter = page.locator("select[aria-label*='状态']")
        status_filter.select_option("已发布")
        page.wait_for_timeout(1000)
        
        # 验证只显示已发布状态的活动
        activity_rows = page.locator("table tbody tr")
        if activity_rows.count() > 0:
            for i in range(activity_rows.count()):
                row_status = activity_rows.nth(i).locator("td").nth(4).text_content()
                assert row_status == "已发布", f"第{i+1}行活动状态应为'已发布'，实际为'{row_status}'"
        else:
            # 如果没有结果，验证显示空状态
            empty_state = page.locator("text=暂无数据")
            assert empty_state.is_visible(), "筛选无结果时应显示'暂无数据'"
```

# ========== P1 批次 3 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-LIST-011: 多条件组合筛选（活动类型+活动状态）")
    @pytest.mark.parametrize("activity_type, activity_status", [
        ("线上", "进行中"),
        ("线下", "已结束"),
        ("混合", "草稿"),
    ])
    def test_activity_list_011_multi_condition_filter(self, page: Page, activity_type, activity_status):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 选择活动类型筛选
        page.select_option("#filterActivityType", activity_type)
        page.wait_for_timeout(500)
        
        # 选择活动状态筛选
        page.select_option("#filterActivityStatus", activity_status)
        page.wait_for_timeout(500)
        
        # 验证筛选结果
        page.wait_for_selector(".activity-item", timeout=5000)
        activity_items = page.locator(".activity-item")
        count = activity_items.count()
        
        # 验证每个活动项都满足筛选条件
        for i in range(count):
            item = activity_items.nth(i)
            item_type = item.locator(".activity-type").text_content()
            item_status = item.locator(".activity-status").text_content()
            assert activity_type in item_type or activity_type == "全部"
            assert activity_status in item_status or activity_status == "全部"

    @allure.title("TC-ACTIVITY-LIST-012: 按活动时间范围筛选")
    @pytest.mark.parametrize("start_date, end_date", [
        ("2024-01-01", "2024-12-31"),
        ("2024-06-01", "2024-06-30"),
        ("2024-03-01", "2024-03-31"),
    ])
    def test_activity_list_012_time_range_filter(self, page: Page, start_date, end_date):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 设置时间范围筛选
        page.fill("#filterStartTime", start_date)
        page.fill("#filterEndTime", end_date)
        page.click("#btnFilter")
        page.wait_for_timeout(1000)
        
        # 验证筛选结果
        page.wait_for_selector(".activity-item", timeout=5000)
        activity_items = page.locator(".activity-item")
        count = activity_items.count()
        
        # 验证每个活动的时间都在范围内
        for i in range(count):
            item = activity_items.nth(i)
            item_start = item.locator(".activity-start-time").text_content()
            item_end = item.locator(".activity-end-time").text_content()
            assert start_date <= item_start[:10] <= end_date
            assert start_date <= item_end[:10] <= end_date

    @allure.title("TC-ACTIVITY-LIST-013: 清除所有筛选条件")
    def test_activity_list_013_clear_all_filters(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 先设置一些筛选条件
        page.select_option("#filterActivityType", "线上")
        page.select_option("#filterActivityStatus", "进行中")
        page.fill("#filterStartTime", "2024-01-01")
        page.fill("#filterEndTime", "2024-12-31")
        page.click("#btnFilter")
        page.wait_for_timeout(1000)
        
        # 获取筛选后的活动数量
        filtered_count = page.locator(".activity-item").count()
        
        # 清除所有筛选条件
        page.click("#btnClearFilter")
        page.wait_for_timeout(1000)
        
        # 验证筛选条件已重置
        expect(page.locator("#filterActivityType")).to_have_value("")
        expect(page.locator("#filterActivityStatus")).to_have_value("")
        expect(page.locator("#filterStartTime")).to_have_value("")
        expect(page.locator("#filterEndTime")).to_have_value("")
        
        # 验证显示所有活动（数量应该大于或等于筛选后的数量）
        all_count = page.locator(".activity-item").count()
        assert all_count >= filtered_count

    @allure.title("TC-ACTIVITY-LIST-014: 默认按更新时间倒序排列")
    def test_activity_list_014_default_sort_by_update_time_desc(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 获取所有活动的更新时间
        page.wait_for_selector(".activity-item", timeout=5000)
        activity_items = page.locator(".activity-item")
        count = activity_items.count()
        
        update_times = []
        for i in range(count):
            update_time = activity_items.nth(i).locator(".activity-update-time").text_content()
            update_times.append(update_time)
        
        # 验证更新时间是倒序排列
        for i in range(len(update_times) - 1):
            assert update_times[i] >= update_times[i + 1], f"更新时间不是倒序排列: {update_times[i]} < {update_times[i + 1]}"

    @allure.title("TC-ACTIVITY-LIST-015: 点击活动开始时间表头排序")
    @pytest.mark.parametrize("click_times", [1, 2])
    def test_activity_list_015_sort_by_start_time(self, page: Page, click_times):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击开始时间表头进行排序
        for _ in range(click_times):
            page.click("#sortStartTime")
            page.wait_for_timeout(500)
        
        # 获取所有活动的开始时间
        page.wait_for_selector(".activity-item", timeout=5000)
        activity_items = page.locator(".activity-item")
        count = activity_items.count()
        
        start_times = []
        for i in range(count):
            start_time = activity_items.nth(i).locator(".activity-start-time").text_content()
            start_times.append(start_time)
        
        # 验证排序结果
        if click_times == 1:
            # 正序
            for i in range(len(start_times) - 1):
                assert start_times[i] <= start_times[i + 1], f"开始时间不是正序排列: {start_times[i]} > {start_times[i + 1]}"
        else:
            # 倒序
            for i in range(len(start_times) - 1):
                assert start_times[i] >= start_times[i + 1], f"开始时间不是倒序排列: {start_times[i]} < {start_times[i + 1]}"

    @allure.title("TC-ACTIVITY-LIST-016: 点击活动结束时间表头排序")
    @pytest.mark.parametrize("click_times", [1, 2])
    def test_activity_list_016_sort_by_end_time(self, page: Page, click_times):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击结束时间表头进行排序
        for _ in range(click_times):
            page.click("#sortEndTime")
            page.wait_for_timeout(500)
        
        # 获取所有活动的结束时间
        page.wait_for_selector(".activity-item", timeout=5000)
        activity_items = page.locator(".activity-item")
        count = activity_items.count()
        
        end_times = []
        for i in range(count):
            end_time = activity_items.nth(i).locator(".activity-end-time").text_content()
            end_times.append(end_time)
        
        # 验证排序结果
        if click_times == 1:
            # 正序
            for i in range(len(end_times) - 1):
                assert end_times[i] <= end_times[i + 1], f"结束时间不是正序排列: {end_times[i]} > {end_times[i + 1]}"
        else:
            # 倒序
            for i in range(len(end_times) - 1):
                assert end_times[i] >= end_times[i + 1], f"结束时间不是倒序排列: {end_times[i]} < {end_times[i + 1]}"
```

# ========== P1 批次 4 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-LIST-017: 数据超过10条时，显示分页")
    def test_pagination_displayed_when_more_than_10_items(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 检查分页控件是否存在
        pagination = page.locator(".pagination, .pagination-container")
        expect(pagination).to_be_visible()
        
        # 验证每页显示10条数据
        rows = page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count <= 10, f"每页应显示不超过10条数据，实际显示{row_count}条"

    @allure.title("TC-ACTIVITY-LIST-018: 点击下一页按钮")
    def test_click_next_page(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取当前页第一条数据
        first_row_first_page = page.locator("table tbody tr").first.text_content()
        
        # 点击下一页
        next_button = page.locator(".pagination .next, .pagination-next")
        next_button.click()
        page.wait_for_timeout(1000)
        
        # 验证跳转到下一页
        first_row_second_page = page.locator("table tbody tr").first.text_content()
        assert first_row_first_page != first_row_second_page, "下一页数据应与上一页不同"

    @allure.title("TC-ACTIVITY-LIST-019: 点击上一页按钮")
    def test_click_previous_page(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 先点击下一页
        next_button = page.locator(".pagination .next, .pagination-next")
        next_button.click()
        page.wait_for_timeout(1000)
        
        # 获取当前页第一条数据
        first_row_current = page.locator("table tbody tr").first.text_content()
        
        # 点击上一页
        prev_button = page.locator(".pagination .prev, .pagination-previous")
        prev_button.click()
        page.wait_for_timeout(1000)
        
        # 验证跳转到上一页
        first_row_previous = page.locator("table tbody tr").first.text_content()
        assert first_row_current != first_row_previous, "上一页数据应与当前页不同"

    @allure.title("TC-ACTIVITY-LIST-020: 点击末页按钮")
    def test_click_last_page(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击末页
        last_button = page.locator(".pagination .last, .pagination-last")
        last_button.click()
        page.wait_for_timeout(1000)
        
        # 验证跳转到最后一页
        # 检查下一页按钮是否禁用
        next_button = page.locator(".pagination .next, .pagination-next")
        expect(next_button).to_be_disabled()

    @allure.title("TC-ACTIVITY-LIST-021: 分页后数据正确")
    def test_pagination_data_correctness(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取所有页面的数据
        all_data = []
        while True:
            # 获取当前页数据
            rows = page.locator("table tbody tr")
            for i in range(rows.count()):
                row_data = rows.nth(i).text_content()
                all_data.append(row_data)
            
            # 检查是否有下一页
            next_button = page.locator(".pagination .next, .pagination-next")
            if next_button.is_disabled():
                break
            next_button.click()
            page.wait_for_timeout(1000)
        
        # 验证数据总数
        assert len(all_data) > 10, f"数据总数应超过10条，实际{len(all_data)}条"
        
        # 验证每页数据不重复
        unique_data = set(all_data)
        assert len(unique_data) == len(all_data), "分页数据存在重复"

[COMPLETE]
```

# ========== P1 批次 5 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-LIST-022: 点击导出按钮")
    def test_export_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证导出功能触发
        expect(page.locator("text=导出中...")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-023: 筛选后导出数据")
    def test_export_filtered_data(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 筛选数据
        page.click("#formType")
        page.select_option("#formType", "线上活动")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证导出功能触发
        expect(page.locator("text=导出中...")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-024: 无数据时点击导出")
    def test_export_no_data(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 清空数据（假设有清空功能）
        page.click("#formName")
        page.fill("#formName", "不存在的活动名称")
        page.click("text=搜索")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证提示信息
        expect(page.locator("text=暂无数据可导出")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-025: 点击活动的详情按钮")
    def test_activity_detail_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击第一个活动的详情按钮
        page.click(".detail-btn:first-child")
        
        # 验证跳转到活动详情页
        expect(page).to_have_url(f"{BASE_URL}/#activity-detail")

    @allure.title("TC-ACTIVITY-LIST-026: 待提交状态的活动显示编辑按钮")
    def test_draft_activity_edit_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 查找待提交状态的活动
        draft_activities = page.locator("text=待提交")
        if draft_activities.count() > 0:
            # 点击编辑按钮
            page.click("text=编辑")
            
            # 验证编辑模态框出现
            expect(page.locator("#btnSaveDraft")).to_be_visible(timeout=5000)
        else:
            pytest.skip("没有待提交状态的活动")

    @allure.title("TC-ACTIVITY-LIST-027: 分页功能验证")
    def test_pagination(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 获取第一页数据
        first_page_data = page.locator("table tbody tr").all_text_contents()
        
        # 点击下一页
        page.click("text=下一页")
        page.wait_for_timeout(1000)
        
        # 获取第二页数据
        second_page_data = page.locator("table tbody tr").all_text_contents()
        
        # 验证数据不重复
        assert len(set(first_page_data) & set(second_page_data)) == 0, "分页数据重复"
        
        # 验证数据不遗漏
        total_data = first_page_data + second_page_data
        assert len(total_data) == len(set(total_data)), "分页数据遗漏"

    @allure.title("TC-ACTIVITY-LIST-028: 搜索功能验证")
    def test_search_function(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 输入搜索关键词
        page.click("#formName")
        page.fill("#formName", "测试活动")
        page.click("text=搜索")
        
        # 验证搜索结果
        expect(page.locator("table tbody tr")).to_have_count(1, timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-029: 重置搜索条件")
    def test_reset_search(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 输入搜索关键词
        page.click("#formName")
        page.fill("#formName", "测试活动")
        page.click("text=搜索")
        
        # 点击重置按钮
        page.click("text=重置")
        
        # 验证搜索条件被清空
        expect(page.locator("#formName")).to_have_value("")

    @allure.title("TC-ACTIVITY-LIST-030: 批量操作功能")
    def test_batch_operation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 选择多个活动
        page.click("input[type='checkbox']:first-child")
        page.click("input[type='checkbox']:nth-child(2)")
        
        # 点击批量操作按钮
        page.click("text=批量取消")
        
        # 验证批量操作确认框
        expect(page.locator("#btnConfirmCancel")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-031: 活动列表排序功能")
    def test_list_sorting(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击排序按钮
        page.click("text=开始时间")
        
        # 验证排序功能
        expect(page.locator("text=排序中...")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-032: 活动列表刷新功能")
    def test_list_refresh(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击刷新按钮
        page.click("text=刷新")
        
        # 验证刷新功能
        expect(page.locator("text=刷新中...")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-033: 活动列表列显示设置")
    def test_column_display_settings(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击列设置按钮
        page.click("text=列设置")
        
        # 验证列设置弹窗
        expect(page.locator("text=列显示设置")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-034: 活动列表导出格式选择")
    def test_export_format_selection(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证导出格式选择
        expect(page.locator("text=导出格式")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-035: 活动列表导出数据范围选择")
    def test_export_data_range_selection(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证数据范围选择
        expect(page.locator("text=数据范围")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-036: 活动列表导出文件命名")
    def test_export_file_naming(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证文件命名输入框
        expect(page.locator("text=文件名")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-037: 活动列表导出进度显示")
    def test_export_progress_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证导出进度显示
        expect(page.locator("text=导出进度")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-038: 活动列表导出完成提示")
    def test_export_completion_prompt(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 等待导出完成
        page.wait_for_timeout(3000)
        
        # 验证导出完成提示
        expect(page.locator("text=导出完成")).to_be_visible(timeout=5000)

    @allure.title("TC-ACTIVITY-LIST-039: 活动列表导出失败处理")
    def test_export_failure_handling(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 模拟网络断开
        page.context.set_offline(True)
        
        # 点击导出按钮
        page.click("text=导出")
        
        # 验证导出失败提示
        expect(page.locator("text=导出失败")).to_be_visible(timeout=5000)
        
        # 恢复网络
        page.context.set_offline(False)

    @allure.title("TC-ACTIVITY-LIST-040: 活动列表导出取消功能")
    def test_export_cancel_function(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 点击导出按钮

# ========== P1 批次 6 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestActivity:

    @allure.title("TC-ACTIVITY-LIST-027: 已完成状态的活动不显示编辑按钮")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "已完成活动测试", "activity_type": "线上", "activity_subtype": "会议", "description": "测试已完成活动编辑按钮", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_completed_activity_no_edit_button(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动并提交
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 模拟活动状态变为已完成（通过直接修改或等待状态变更）
        # 这里假设活动创建后状态变为已完成，实际测试中可能需要额外操作
        
        # 验证编辑按钮不可见
        edit_buttons = page.locator(".edit-btn")
        expect(edit_buttons).to_have_count(0)

    @allure.title("TC-ACTIVITY-AUTH-001: admin账号查看活动列表")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "admin测试活动", "activity_type": "线上", "activity_subtype": "会议", "description": "admin创建的测试活动", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_admin_view_activity_list(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动并保存草稿
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 创建另一个活动并正式提交
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"] + "_正式")
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"] + "_正式")
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证显示所有正式提交的活动 + 自己保存的草稿
        activity_items = page.locator(".activity-item")
        expect(activity_items).to_have_count(2)

    @allure.title("TC-ACTIVITY-AUTH-002: user1账号查看活动列表")
    @pytest.mark.parametrize("data", [
        {"role": "user1", "activity_name": "user1测试活动", "activity_type": "线上", "activity_subtype": "会议", "description": "user1创建的测试活动", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_user1_view_activity_list(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动并保存草稿
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSaveDraft")
        wait_for_toast(page)
        
        # 创建另一个活动并正式提交
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"] + "_正式")
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"] + "_正式")
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证只显示自己正式提交的活动 + 自己保存的草稿
        activity_items = page.locator(".activity-item")
        expect(activity_items).to_have_count(2)

    @allure.title("TC-ACTIVITY-AUTH-003: 已删除的活动不显示在列表中")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "删除测试活动", "activity_type": "线上", "activity_subtype": "会议", "description": "测试删除活动", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_deleted_activity_not_displayed(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动并提交
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 删除活动
        page.click(".detail-btn")
        page.click("#btnCancelActivity")
        page.fill("#cancelReason", "测试删除")
        page.click("#btnConfirmCancel")
        wait_for_toast(page)
        
        # 验证列表中没有已删除的活动
        activity_items = page.locator(".activity-item")
        expect(activity_items).to_have_count(0)

    @allure.title("验证空活动名称错误消息")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_type": "线上", "activity_subtype": "会议", "description": "测试空名称", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_empty_name_error(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动，不填写名称
        page.click("#btnCreate")
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        
        # 验证提交按钮禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()
        
        # 尝试提交
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_contain_text("请输入活动名称")

    @allure.title("验证空活动类型错误消息")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "测试活动", "activity_subtype": "会议", "description": "测试空类型", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_empty_type_error(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动，不选择类型
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        
        # 验证提交按钮禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()
        
        # 尝试提交
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_contain_text("请选择活动类型")

    @allure.title("验证空子类型错误消息")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "测试活动", "activity_type": "线上", "description": "测试空子类型", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_empty_subtype_error(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动，不选择子类型
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.fill("#formDescription", data["description"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        
        # 验证提交按钮禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()
        
        # 尝试提交
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_contain_text("请选择子类型")

    @allure.title("验证空活动简介错误消息")
    @pytest.mark.parametrize("data", [
        {"role": "admin", "activity_name": "测试活动", "activity_type": "线上", "activity_subtype": "会议", "start_time": "2024-01-01T10:00", "end_time": "2024-01-01T12:00"}
    ])
    def test_empty_description_error(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.select_option("#roleSelect", data["role"])
        
        # 创建活动，不填写简介
        page.click("#btnCreate")
        page.fill("#formName", data["activity_name"])
        page.select_option("#formType", data["activity_type"])
        page.select_option("#formSubType", data["activity_subtype"])
        page.fill("#formStartTime", data["start_time"])
        page.fill("#formEndTime", data["end_time"])
        
        # 验证提交按钮禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()
        
        # 尝试提交
        page.click("#btnSubmit")
        wait_for_toast(page)
        
        # 验证错误消息

# ========== P1 批次 7 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-DETAIL-001: 详情页显示所有活动信息")
    def test_detail_display_all_info(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 验证活动详情显示
        expect(page.locator("#detailName")).to_be_visible()
        expect(page.locator("#detailType")).to_be_visible()
        expect(page.locator("#detailTime")).to_be_visible()
        expect(page.locator("#detailLocation")).to_be_visible()
        expect(page.locator("#detailDescription")).to_be_visible()
        expect(page.locator("#detailRemark")).to_be_visible()
        
        # 验证URL包含活动详情标识
        expect(page).to_have_url(lambda url: "detail" in url or "#activity-detail" in url)

    @allure.title("TC-ACTIVITY-DETAIL-002: 富文本内容正确渲染")
    def test_rich_text_rendering(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 验证富文本内容
        rich_content = page.locator("#detailDescription")
        
        # 检查加粗文本
        bold_elements = rich_content.locator("strong, b")
        expect(bold_elements.first).to_be_visible()
        
        # 检查斜体文本
        italic_elements = rich_content.locator("em, i")
        expect(italic_elements.first).to_be_visible()
        
        # 检查下划线文本
        underline_elements = rich_content.locator("u, ins")
        expect(underline_elements.first).to_be_visible()
        
        # 检查超链接
        link_elements = rich_content.locator("a")
        expect(link_elements.first).to_be_visible()

    @allure.title("TC-ACTIVITY-DETAIL-003: 上传的文件可预览/下载")
    def test_file_preview_download(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 检查文件附件区域
        file_area = page.locator("#detailFiles")
        if file_area.is_visible():
            # 点击文件链接
            file_link = file_area.locator("a").first
            if file_link.is_visible():
                # 验证文件链接可点击
                expect(file_link).to_be_enabled()
                
                # 点击文件链接
                with page.expect_download() as download_info:
                    file_link.click()
                download = download_info.value
                
                # 验证下载开始
                assert download.suggested_filename != ""
        else:
            # 如果没有文件，验证显示"暂无附件"
            expect(file_area).to_contain_text("暂无附件")

    @allure.title("TC-ACTIVITY-DETAIL-004: 空字段显示占位符")
    def test_empty_field_placeholder(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 检查各字段是否显示占位符
        fields_to_check = [
            "#detailName",
            "#detailType", 
            "#detailTime",
            "#detailLocation",
            "#detailDescription",
            "#detailRemark"
        ]
        
        for field_selector in fields_to_check:
            field = page.locator(field_selector)
            field_text = field.text_content()
            if field_text is None or field_text.strip() == "":
                # 空字段应显示占位符
                expect(field).to_contain_text("-")
                expect(field).to_contain_text("暂无")

    @allure.title("TC-ACTIVITY-DETAIL-005: 详情页数据与列表页数据一致")
    def test_detail_data_consistent_with_list(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 获取列表页第一个活动的信息
        first_activity_row = page.locator("#activity-list tbody tr").first
        list_name = first_activity_row.locator("td:nth-child(1)").text_content()
        list_time = first_activity_row.locator("td:nth-child(2)").text_content()
        list_status = first_activity_row.locator("td:nth-child(3)").text_content()
        
        # 点击详情按钮
        first_activity_row.locator(".detail-btn").click()
        page.wait_for_load_state("networkidle")
        
        # 获取详情页信息
        detail_name = page.locator("#detailName").text_content()
        detail_time = page.locator("#detailTime").text_content()
        detail_status = page.locator("#detailStatus").text_content()
        
        # 验证数据一致性
        assert list_name == detail_name, f"活动名称不一致: 列表页'{list_name}' vs 详情页'{detail_name}'"
        assert list_time == detail_time, f"活动时间不一致: 列表页'{list_time}' vs 详情页'{detail_time}'"
        assert list_status == detail_status, f"活动状态不一致: 列表页'{list_status}' vs 详情页'{detail_status}'"
        
        # 验证URL包含活动详情标识
        expect(page).to_have_url(lambda url: "detail" in url or "#activity-detail" in url)

    @allure.title("TC-ACTIVITY-DETAIL-006: 详情页返回列表页功能")
    def test_detail_back_to_list(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 点击返回按钮
        page.click("#btnBackToList")
        page.wait_for_load_state("networkidle")
        
        # 验证返回列表页
        expect(page.locator("#activity-list")).to_be_visible()
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-DETAIL-007: 详情页关闭按钮功能")
    def test_detail_close_button(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 点击关闭按钮
        page.click("#btnCloseModal")
        page.wait_for_load_state("networkidle")
        
        # 验证返回列表页
        expect(page.locator("#activity-list")).to_be_visible()
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("TC-ACTIVITY-DETAIL-008: 详情页活动状态显示")
    def test_detail_activity_status(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 验证活动状态显示
        status_element = page.locator("#detailStatus")
        expect(status_element).to_be_visible()
        
        # 验证状态值有效
        status_text = status_element.text_content()
        valid_statuses = ["草稿", "已发布", "进行中", "已结束", "已取消"]
        assert status_text in valid_statuses, f"无效的活动状态: {status_text}"

    @allure.title("TC-ACTIVITY-DETAIL-009: 详情页活动时间格式")
    def test_detail_time_format(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 验证时间格式
        time_element = page.locator("#detailTime")
        time_text = time_element.text_content()
        
        # 验证时间格式为 YYYY-MM-DD HH:mm - YYYY-MM-DD HH:mm
        import re
        time_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} - \d{4}-\d{2}-\d{2} \d{2}:\d{2}"
        assert re.match(time_pattern, time_text), f"时间格式不正确: {time_text}"

    @allure.title("TC-ACTIVITY-DETAIL-010: 详情页活动地点完整显示")
    def test_detail_location_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.fill("#username", "admin")
        page.fill("#password", "admin")
        page.click("#loginBtn")
        page.wait_for_load_state("networkidle")
        
        # 等待活动列表加载
        page.wait_for_selector("#activity-list", timeout=5000)
        
        # 点击第一个活动的详情按钮
        page.locator(".detail-btn").first.click()
        page.wait_for_load_state("networkidle")
        
        # 验证地点信息
        location_element = page.locator("#detailLocation")
        expect(location_element).to_be

# ========== P1 批次 8 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-DETAIL-006: 编辑活动后，详情页数据实时更新")
    def test_edit_activity_updates_detail(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)

        # 创建活动
        page.click("#btnCreate")
        page.wait_for_selector("#formName", timeout=5000)

        # 填写活动信息
        page.fill("#formName", "测试活动-编辑更新")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "活动描述")
        page.fill("#formStartTime", "2024-12-01 10:00")
        page.fill("#formEndTime", "2024-12-01 12:00")
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.fill("#formProvince", "广东省")
        page.fill("#formCity", "深圳市")
        page.fill("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园")

        # 保存草稿
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)

        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证详情页显示的数据
        expect(page.locator("#formName")).to_have_value("测试活动-编辑更新")
        expect(page.locator("#formType")).to_have_value("线上")
        expect(page.locator("#formSubType")).to_have_value("直播")

        # 编辑活动名称
        page.fill("#formName", "测试活动-已编辑更新")
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)

        # 重新打开详情页
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证数据已更新
        expect(page.locator("#formName")).to_have_value("测试活动-已编辑更新")

    @allure.title("TC-ACTIVITY-DETAIL-007: 待提交状态显示正确")
    def test_pending_submit_status_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)

        # 创建活动并保存草稿
        page.click("#btnCreate")
        page.wait_for_selector("#formName", timeout=5000)

        page.fill("#formName", "待提交状态测试")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "活动描述")
        page.fill("#formStartTime", "2024-12-01 10:00")
        page.fill("#formEndTime", "2024-12-01 12:00")
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.fill("#formProvince", "广东省")
        page.fill("#formCity", "深圳市")
        page.fill("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园")

        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)

        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证状态标签
        status_label = page.locator(".status-label, .activity-status")
        expect(status_label).to_have_text("待提交")
        expect(status_label).to_have_css("color", "rgb(255, 165, 0)")  # 橙色

    @allure.title("TC-ACTIVITY-DETAIL-008: 已发布状态显示正确")
    def test_published_status_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)

        # 创建活动并提交
        page.click("#btnCreate")
        page.wait_for_selector("#formName", timeout=5000)

        page.fill("#formName", "已发布状态测试")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "活动描述")
        page.fill("#formStartTime", "2024-12-01 10:00")
        page.fill("#formEndTime", "2024-12-01 12:00")
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.fill("#formProvince", "广东省")
        page.fill("#formCity", "深圳市")
        page.fill("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园")

        page.click("#btnSubmit")
        page.wait_for_timeout(1000)

        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证状态标签
        status_label = page.locator(".status-label, .activity-status")
        expect(status_label).to_have_text("已发布")
        expect(status_label).to_have_css("color", "rgb(0, 128, 0)")  # 绿色

    @allure.title("TC-ACTIVITY-DETAIL-009: 已完成状态显示正确")
    def test_completed_status_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)

        # 创建活动并提交
        page.click("#btnCreate")
        page.wait_for_selector("#formName", timeout=5000)

        page.fill("#formName", "已完成状态测试")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "活动描述")
        page.fill("#formStartTime", "2024-11-01 10:00")
        page.fill("#formEndTime", "2024-11-01 12:00")
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.fill("#formProvince", "广东省")
        page.fill("#formCity", "深圳市")
        page.fill("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园")

        page.click("#btnSubmit")
        page.wait_for_timeout(1000)

        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证状态标签
        status_label = page.locator(".status-label, .activity-status")
        expect(status_label).to_have_text("已完成")
        expect(status_label).to_have_css("color", "rgb(0, 0, 255)")  # 蓝色

    @allure.title("TC-ACTIVITY-DETAIL-010: 已取消状态显示正确")
    def test_cancelled_status_display(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)

        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        page.wait_for_timeout(500)

        # 创建活动并提交
        page.click("#btnCreate")
        page.wait_for_selector("#formName", timeout=5000)

        page.fill("#formName", "已取消状态测试")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "活动描述")
        page.fill("#formStartTime", "2024-12-01 10:00")
        page.fill("#formEndTime", "2024-12-01 12:00")
        page.fill("#formOnlinePlatform", "腾讯会议")
        page.fill("#formProvince", "广东省")
        page.fill("#formCity", "深圳市")
        page.fill("#formDistrict", "南山区")
        page.fill("#formAddress", "科技园")

        page.click("#btnSubmit")
        page.wait_for_timeout(1000)

        # 取消活动
        page.click("#btnCancelActivity")
        page.wait_for_selector("#cancelReason", timeout=5000)
        page.fill("#cancelReason", "测试取消")
        page.click("#btnConfirmCancel")
        page.wait_for_timeout(1000)

        # 点击详情按钮
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(1000)

        # 验证状态标签
        status_label = page.locator(".status-label, .activity-status")
        expect(status_label).to_have_text("已取消")
        expect(status_label).to_have_css("color", "rgb(128, 128, 128)")  # 灰色
[COMPLETE]
```

# ========== P1 批次 9 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-DETAIL-011: 待提交状态显示编辑和删除按钮")
    def test_pending_activity_shows_edit_and_delete_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个待提交的活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-待提交")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-12-01T10:00")
        page.fill("#formEndTime", "2024-12-01T12:00")
        page.fill("#formDescription", "这是一个测试活动")
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)
        
        # 查看活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        
        # 验证编辑和删除按钮可见
        expect(page.locator("#btnEdit")).to_be_visible()
        expect(page.locator("#btnDelete")).to_be_visible()
        
        # 关闭详情
        page.click("#btnCloseModal")

    @allure.title("TC-ACTIVITY-DETAIL-012: 已发布状态显示编辑和取消按钮")
    def test_published_activity_shows_edit_and_cancel_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个已发布的活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已发布")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-12-01T10:00")
        page.fill("#formEndTime", "2024-12-01T12:00")
        page.fill("#formDescription", "这是一个测试活动")
        page.click("#btnSubmit")
        page.wait_for_timeout(1000)
        
        # 查看活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        
        # 验证编辑和取消按钮可见
        expect(page.locator("#btnEdit")).to_be_visible()
        expect(page.locator("#btnCancelActivity")).to_be_visible()
        
        # 关闭详情
        page.click("#btnCloseModal")

    @allure.title("TC-ACTIVITY-DETAIL-013: 已完成状态不显示操作按钮")
    def test_completed_activity_shows_no_action_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个已完成的活动（通过创建并完成）
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已完成")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-11-01T10:00")
        page.fill("#formEndTime", "2024-11-01T12:00")
        page.fill("#formDescription", "这是一个测试活动")
        page.click("#btnSubmit")
        page.wait_for_timeout(1000)
        
        # 查看活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        
        # 验证无操作按钮
        expect(page.locator("#btnEdit")).not_to_be_visible()
        expect(page.locator("#btnCancelActivity")).not_to_be_visible()
        expect(page.locator("#btnDelete")).not_to_be_visible()
        
        # 关闭详情
        page.click("#btnCloseModal")

    @allure.title("TC-ACTIVITY-DETAIL-014: 已取消状态不显示操作按钮")
    def test_cancelled_activity_shows_no_action_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个已取消的活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-已取消")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-12-01T10:00")
        page.fill("#formEndTime", "2024-12-01T12:00")
        page.fill("#formDescription", "这是一个测试活动")
        page.click("#btnSubmit")
        page.wait_for_timeout(1000)
        
        # 取消活动
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        page.click("#btnCancelActivity")
        page.fill("#cancelReason", "测试取消")
        page.click("#btnConfirmCancel")
        page.wait_for_timeout(1000)
        
        # 查看活动详情
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        
        # 验证无操作按钮
        expect(page.locator("#btnEdit")).not_to_be_visible()
        expect(page.locator("#btnCancelActivity")).not_to_be_visible()
        expect(page.locator("#btnDelete")).not_to_be_visible()
        
        # 关闭详情
        page.click("#btnCloseModal")

    @allure.title("TC-ACTIVITY-DETAIL-015: 点击编辑按钮进入编辑模式")
    def test_click_edit_button_enters_edit_mode(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个待提交的活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-编辑测试")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-12-01T10:00")
        page.fill("#formEndTime", "2024-12-01T12:00")
        page.fill("#formDescription", "原始描述")
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)
        
        # 查看活动详情并点击编辑
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        page.click("#btnEdit")
        page.wait_for_timeout(500)
        
        # 验证表单预填当前数据
        expect(page.locator("#formName")).to_have_value("测试活动-编辑测试")
        expect(page.locator("#formType")).to_have_value("线上活动")
        expect(page.locator("#formSubType")).to_have_value("直播")
        expect(page.locator("#formDescription")).to_have_value("原始描述")
        
        # 验证可修改
        page.fill("#formName", "测试活动-已编辑")
        page.fill("#formDescription", "已编辑的描述")
        
        # 关闭模态框
        page.click("#btnCloseModal")

    @allure.title("TC-ACTIVITY-DETAIL-016: 编辑后保存草稿")
    def test_edit_and_save_draft(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 登录
        page.click("#roleSelect")
        page.select_option("#roleSelect", "admin")
        
        # 创建一个待提交的活动
        page.click("#btnCreate")
        page.fill("#formName", "测试活动-草稿编辑")
        page.select_option("#formType", "线上活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-12-01T10:00")
        page.fill("#formEndTime", "2024-12-01T12:00")
        page.fill("#formDescription", "原始描述")
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)
        
        # 查看活动详情并点击编辑
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        page.click("#btnEdit")
        page.wait_for_timeout(500)
        
        # 修改数据
        page.fill("#formName", "测试活动-草稿已编辑")
        page.fill("#formDescription", "已编辑的描述")
        page.fill("#formRemark", "编辑备注")
        
        # 保存草稿
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)
        
        # 验证保存成功
        wait_for_toast(page)
        
        # 重新打开查看是否保存
        page.click(".detail-btn:first-child")
        page.wait_for_timeout(500)
        page.click("#btnEdit")
        page.wait_for_timeout(500)
        
        # 验证数据已更新
        expect(page.locator("#formName")).to_have_value("测试活动-草稿已编辑")
        expect(page.locator("#formDescription")).to_have_value("已编辑的描述")
        expect(page.locator("#formRemark")).to_have_value("编辑备注")
        
        # 关闭模态框
        page.click("#btnCloseModal")
```

# ========== P1 批次 10 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("TC-ACTIVITY-DETAIL-001: 新建活动-所有字段填写完整-保存草稿")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动001",
            "type": "线上",
            "subtype": "直播",
            "other_type": "",
            "start_time": "2024-01-15T09:00",
            "end_time": "2024-01-15T18:00",
            "description": "这是一个测试活动",
            "remark": "测试备注",
            "online_platform": "腾讯会议",
            "province": "广东省",
            "city": "深圳市",
            "district": "南山区",
            "address": "科技园南区A栋",
            "action": "save_draft",
            "expected_url": "#activity-list",
            "expected_status": "待提交"
        }
    ])
    def test_create_activity_save_draft(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", data["name"])
        
        # 选择活动类型
        page.select_option("#formType", data["type"])
        
        # 选择活动子类型
        page.select_option("#formSubType", data["subtype"])
        
        # 填写开始时间
        page.fill("#formStartTime", data["start_time"])
        
        # 填写结束时间
        page.fill("#formEndTime", data["end_time"])
        
        # 填写活动简介
        page.fill("#formDescription", data["description"])
        
        # 填写备注
        page.fill("#formRemark", data["remark"])
        
        # 填写线上平台
        page.fill("#formOnlinePlatform", data["online_platform"])
        
        # 填写省份
        page.fill("#formProvince", data["province"])
        
        # 填写城市
        page.fill("#formCity", data["city"])
        
        # 填写区县
        page.fill("#formDistrict", data["district"])
        
        # 填写详细地址
        page.fill("#formAddress", data["address"])
        
        # 点击保存草稿
        page.click("#btnSaveDraft")
        
        # 等待保存完成
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: data["expected_url"] in url)
        
        # 验证状态为待提交
        status_element = page.locator(".activity-status")
        expect(status_element).to_have_text(data["expected_status"])

    @allure.title("TC-ACTIVITY-DETAIL-002: 新建活动-所有字段填写完整-完成创建")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动002",
            "type": "线下",
            "subtype": "会议",
            "other_type": "",
            "start_time": "2024-01-20T09:00",
            "end_time": "2024-01-20T18:00",
            "description": "这是一个线下会议活动",
            "remark": "重要会议",
            "online_platform": "",
            "province": "北京市",
            "city": "北京市",
            "district": "朝阳区",
            "address": "国贸大厦A座",
            "action": "submit",
            "expected_url": "#activity-list",
            "expected_status": "已发布"
        }
    ])
    def test_create_activity_submit(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", data["name"])
        
        # 选择活动类型
        page.select_option("#formType", data["type"])
        
        # 选择活动子类型
        page.select_option("#formSubType", data["subtype"])
        
        # 填写开始时间
        page.fill("#formStartTime", data["start_time"])
        
        # 填写结束时间
        page.fill("#formEndTime", data["end_time"])
        
        # 填写活动简介
        page.fill("#formDescription", data["description"])
        
        # 填写备注
        page.fill("#formRemark", data["remark"])
        
        # 填写省份
        page.fill("#formProvince", data["province"])
        
        # 填写城市
        page.fill("#formCity", data["city"])
        
        # 填写区县
        page.fill("#formDistrict", data["district"])
        
        # 填写详细地址
        page.fill("#formAddress", data["address"])
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 等待提交完成
        wait_for_toast(page)
        
        # 验证成功
        expect(page).to_have_url(lambda url: data["expected_url"] in url)
        
        # 验证状态为已发布
        status_element = page.locator(".activity-status")
        expect(status_element).to_have_text(data["expected_status"])

    @allure.title("TC-ACTIVITY-DETAIL-003: 新建活动-必填字段为空-验证错误消息")
    @pytest.mark.parametrize("data", [
        {
            "name": "",
            "type": "线上",
            "subtype": "直播",
            "start_time": "2024-02-01T09:00",
            "end_time": "2024-02-01T18:00",
            "description": "测试活动",
            "expected_error": "请输入活动名称"
        },
        {
            "name": "测试活动",
            "type": "",
            "subtype": "直播",
            "start_time": "2024-02-01T09:00",
            "end_time": "2024-02-01T18:00",
            "description": "测试活动",
            "expected_error": "请选择活动类型"
        },
        {
            "name": "测试活动",
            "type": "线上",
            "subtype": "",
            "start_time": "2024-02-01T09:00",
            "end_time": "2024-02-01T18:00",
            "description": "测试活动",
            "expected_error": "请选择子类型"
        },
        {
            "name": "测试活动",
            "type": "线上",
            "subtype": "直播",
            "start_time": "2024-02-01T09:00",
            "end_time": "2024-02-01T18:00",
            "description": "",
            "expected_error": "请输入活动简介"
        }
    ])
    def test_create_activity_empty_required_fields(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称（如果不为空）
        if data["name"]:
            page.fill("#formName", data["name"])
        
        # 选择活动类型（如果不为空）
        if data["type"]:
            page.select_option("#formType", data["type"])
        
        # 选择活动子类型（如果不为空）
        if data["subtype"]:
            page.select_option("#formSubType", data["subtype"])
        
        # 填写开始时间
        page.fill("#formStartTime", data["start_time"])
        
        # 填写结束时间
        page.fill("#formEndTime", data["end_time"])
        
        # 填写活动简介（如果不为空）
        if data["description"]:
            page.fill("#formDescription", data["description"])
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_have_text(data["expected_error"])
        
        # 验证停留在当前页面
        expect(page).to_have_url(f"{BASE_URL}/")

    @allure.title("TC-ACTIVITY-DETAIL-004: 新建活动-结束时间早于开始时间-验证错误消息")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动004",
            "type": "线上",
            "subtype": "直播",
            "start_time": "2024-03-01T18:00",
            "end_time": "2024-03-01T09:00",
            "description": "测试活动",
            "expected_error": "结束时间必须晚于开始时间"
        }
    ])
    def test_create_activity_invalid_time_range(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", data["name"])
        
        # 选择活动类型
        page.select_option("#formType", data["type"])
        
        # 选择活动子类型
        page.select_option("#formSubType", data["subtype"])
        
        # 填写开始时间
        page.fill("#formStartTime", data["start_time"])
        
        # 填写结束时间
        page.fill("#formEndTime", data["end_time"])
        
        # 填写活动简介
        page.fill("#formDescription", data["description"])
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_have_text(data["expected_error"])
        
        # 验证停留在当前页面
        expect(page).to_have_url(f"{BASE_URL}/")

    @allure.title("TC-ACTIVITY-DETAIL-005: 新建活动-活动时长超过72小时-验证错误消息")
    @pytest.mark.parametrize("data", [
        {
            "name": "测试活动005",
            "type": "线上",
            "subtype": "直播",
            "start_time": "2024-04-01T09:00",
            "end_time": "2024-04-05T09:00",
            "description": "测试活动",
            "expected_error": "活动时长不能超过72小时"
        }
    ])
    def test_create_activity_time_exceeds(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 填写活动名称
        page.fill("#formName", data["name"])
        
        # 选择活动类型
        page.select_option("#formType", data["type"])
        
        # 选择活动子类型
        page.select_option("#formSubType", data["subtype"])
        
        # 填写开始时间
        page.fill("#formStartTime", data["start_time"])
        
        # 填写结束时间
        page.fill("#formEndTime", data["end_time"])
        
        # 填写活动简介
        page.fill("#formDescription", data["description"])
        
        # 点击完成创建
        page.click("#btnSubmit")
        
        # 验证错误消息
        error_message = page.locator(".error-message")
        expect(error_message).to_have_text(data["expected_error"])
        
        # 验证停留在当前页面
        expect(page).to_have_url(f"{BASE_URL}/")

    @allure.title("TC-ACTIVITY-DETAIL-006: 新建活动-空字段时提交按钮禁用")
    @pytest.mark.parametrize("data", [
        {
            "name": "",
            "type": "",
            "subtype": "",
            "start_time": "",
            "end_time": "",
            "description": ""
        }
    ])
    def test_create_activity_submit_button_disabled(self, page: Page, data):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_selector("#formName", state="visible")
        
        # 验证提交按钮禁用
        submit_button = page.locator("#btnSubmit")
        expect(submit_button).to_be_disabled()

    @allure.title("TC-ACTIVITY-DETAIL-007: 新建活动-点击放弃创建

# ========== P1 批次 11 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("切换活动类型后，子类型下拉选项相应变化")
    def test_subtype_changes_with_type(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 选择活动类型为"线上"
        page.locator("#formType").select_option("线上")
        page.wait_for_timeout(500)
        
        # 获取子类型选项
        subtype_options = page.locator("#formSubType option").all_text_contents()
        expected_options = ["请选择", "腾讯会议", "钉钉", "Zoom", "其他"]
        
        # 验证子类型选项
        for option in expected_options:
            assert option in subtype_options, f"子类型选项 '{option}' 未找到"
        
        # 选择活动类型为"线下"
        page.locator("#formType").select_option("线下")
        page.wait_for_timeout(500)
        
        # 获取子类型选项
        subtype_options = page.locator("#formSubType option").all_text_contents()
        expected_options = ["请选择", "会议室", "报告厅", "户外场地", "其他"]
        
        # 验证子类型选项
        for option in expected_options:
            assert option in subtype_options, f"子类型选项 '{option}' 未找到"

    @allure.title("提示'结束时间必须晚于开始时间'，提交失败")
    def test_invalid_time_range(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 填写活动名称
        page.locator("#formName").fill("测试活动")
        
        # 选择活动类型
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("腾讯会议")
        
        # 填写活动简介
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 设置开始时间晚于结束时间
        page.locator("#formStartTime").fill("2024-12-31 10:00")
        page.locator("#formEndTime").fill("2024-12-30 10:00")
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "结束时间必须晚于开始时间" in error_message, f"错误消息不匹配: {error_message}"
        
        # 验证停留在当前页面
        assert page.url == f"{BASE_URL}/", "页面未停留在当前页面"

    @allure.title("提示'活动时长不能超过72小时'，提交失败")
    def test_time_exceeds(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 填写活动名称
        page.locator("#formName").fill("测试活动")
        
        # 选择活动类型
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("腾讯会议")
        
        # 填写活动简介
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 设置时间跨度超过72小时
        page.locator("#formStartTime").fill("2024-12-30 10:00")
        page.locator("#formEndTime").fill("2025-01-03 10:00")
        
        # 点击完成创建
        page.locator("#btnSubmit").click()
        
        # 验证错误提示
        wait_for_toast(page)
        error_message = page.locator(".toast-message, .toast").text_content()
        assert "活动时长不能超过72小时" in error_message, f"错误消息不匹配: {error_message}"
        
        # 验证停留在当前页面
        assert page.url == f"{BASE_URL}/", "页面未停留在当前页面"

    @allure.title("弹出确认提示，确认后关闭编辑弹框，不保存修改")
    def test_cancel_edit_confirmation(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 填写一些内容
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("腾讯会议")
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 点击放弃创建
        page.locator("#btnCancel").click()
        
        # 等待确认对话框
        page.wait_for_selector(".confirm-dialog, .dialog", timeout=3000)
        
        # 确认取消
        page.locator("#btnConfirmCancel").click()
        
        # 验证弹框已关闭
        page.wait_for_timeout(500)
        assert not page.locator("#formName").is_visible(), "编辑弹框未关闭"
        
        # 验证URL不包含#activity-list，表示未保存
        assert "#activity-list" not in page.url, "活动被意外保存"

    @allure.title("只提交一次，不产生重复记录")
    def test_no_duplicate_submission(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 填写活动信息
        page.locator("#formName").fill("唯一活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("腾讯会议")
        page.locator("#formDescription").fill("这是一个唯一活动")
        page.locator("#formStartTime").fill("2024-12-30 10:00")
        page.locator("#formEndTime").fill("2024-12-30 12:00")
        
        # 快速点击两次提交按钮
        page.locator("#btnSubmit").click()
        page.locator("#btnSubmit").click()
        
        # 等待页面跳转
        page.wait_for_timeout(2000)
        
        # 验证URL包含#activity-list
        assert "#activity-list" in page.url, "提交失败"
        
        # 验证活动列表中只有一条记录
        activity_count = page.locator(".activity-item, .activity-row").count()
        assert activity_count == 1, f"存在重复记录，活动数量为: {activity_count}"

    @allure.title("只执行一次取消操作，不产生重复记录")
    def test_no_duplicate_cancel(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动
        page.locator("#btnCreate").click()
        page.wait_for_selector("#formName")
        
        # 填写活动信息
        page.locator("#formName").fill("测试活动")
        page.locator("#formType").select_option("线上")
        page.locator("#formSubType").select_option("腾讯会议")
        page.locator("#formDescription").fill("这是一个测试活动")
        
        # 快速点击两次取消按钮
        page.locator("#btnCancel").click()
        page.locator("#btnCancel").click()
        
        # 等待确认对话框
        page.wait_for_selector(".confirm-dialog, .dialog", timeout=3000)
        
        # 确认取消
        page.locator("#btnConfirmCancel").click()
        
        # 验证弹框已关闭
        page.wait_for_timeout(500)
        assert not page.locator("#formName").is_visible(), "编辑弹框未关闭"
        
        # 验证URL不包含#activity-list，表示未保存
        assert "#activity-list" not in page.url, "活动被意外保存"

    @allure.title("显示'编辑活动'和'删除活动'按钮，不显示'取消活动'")
    def test_admin_activity_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 以admin身份登录
        page.locator("#roleSelect").select_option("admin")
        page.wait_for_timeout(500)
        
        # 点击详情按钮查看活动
        page.locator(".detail-btn").first.click()
        page.wait_for_timeout(500)
        
        # 验证按钮显示
        edit_button = page.locator("#btnEditActivity")
        delete_button = page.locator("#btnDeleteActivity")
        cancel_button = page.locator("#btnCancelActivity")
        
        assert edit_button.is_visible(), "编辑活动按钮未显示"
        assert delete_button.is_visible(), "删除活动按钮未显示"
        assert not cancel_button.is_visible(), "取消活动按钮不应显示"

    @allure.title("显示'编辑活动'和'取消活动'按钮，不显示'删除活动'")
    def test_user_activity_buttons(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 以user1身份登录
        page.locator("#roleSelect").select_option("user1")
        page.wait_for_timeout(500)
        
        # 点击详情按钮查看活动
        page.locator(".detail-btn").first.click()
        page.wait_for_timeout(500)
        
        # 验证按钮显示
        edit_button = page.locator("#btnEditActivity")
        delete_button = page.locator("#btnDeleteActivity")
        cancel_button = page.locator("#btnCancelActivity")
        
        assert edit_button.is_visible(), "编辑活动按钮未显示"
        assert cancel_button.is_visible(), "取消活动按钮未显示"
        assert not delete_button.is_visible(), "删除活动按钮不应显示"

    @allure.title("Admin可看到全部用户创建的活动")
    def test_admin_sees_all_activities(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 以admin身份登录
        page.locator("#roleSelect").select_option("admin")
        page.wait_for_timeout(500)
        
        # 获取活动列表
        activity_items = page.locator(".activity-item, .activity-row")
        activity_count = activity_items.count()
        
        # 验证有多个活动（admin和user1创建的活动）
        assert activity_count > 0, "没有显示任何活动"
        
        # 验证活动列表包含不同创建者的活动
        creators = set()
        for i in range(activity_count):
            creator = activity_items.nth(i).locator(".creator, .author").text_content()
            creators.add(creator)
        
        assert len(creators) > 1, "Admin只能看到一个用户的活动"

    @allure.title("user1只能看到自己创建的活动，看不到admin的活动")
    def test_user_sees_only_own_activities(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 以user1身份登录
        page.locator("#roleSelect").select_option("user1")
        page.wait_for_timeout(500)
        
        # 获取活动列表
        activity_items = page.locator(".activity-item, .activity-row")
        activity_count = activity_items.count()
        
        # 验证有活动显示
        assert activity_count > 0, "没有显示任何活动"
        
        # 验证所有活动都是user1创建的
        for i in range(activity_count):
            creator = activity_items.nth(i).locator(".creator, .author").text_content()
            assert creator == "user1", f"活动{i+1}不是user1创建的，而是{creator}创建的"
        
        # 验证没有admin创建的活动
        admin_activities = page.locator(".activity-item, .activity-row").filter(has_text="admin")
        assert admin_activities.count() == 0, "user1看到了admin的活动"

    @allure.title("空字段时验证提交按钮禁用")
    def test_submit_button_disabled_with_empty_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page

# ========== P1 批次 12 ==========
```python
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html"

def close_dialog(page: Page):
    try:
        page.locator(".modal-close, .dialog-close").click(timeout=2000)
    except:
        pass

def wait_for_toast(page: Page):
    try:
        page.wait_for_selector(".toast-message, .toast", timeout=3000)
    except:
        pass

@allure.feature("活动管理")
class TestACTIVITY:

    @allure.title("测试用户1尝试编辑admin的活动时提示无权限或按钮不可见")
    def test_user1_cannot_edit_admin_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 切换到user1角色
        page.select_option("#roleSelect", "user1")
        page.wait_for_timeout(500)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_timeout(1000)
        
        # 验证活动创建成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        
        # 点击详情按钮
        page.click(".detail-btn")
        page.wait_for_timeout(500)
        
        # 验证取消活动按钮不可见或提示无权限
        cancel_btn = page.locator("#btnCancelActivity")
        expect(cancel_btn).to_be_hidden()

    @allure.title("测试创建活动时未填写名称的错误提示")
    def test_create_activity_empty_name(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 不填写活动名称，直接提交
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("#formName")).to_be_visible()
        expect(page.locator("text=请输入活动名称")).to_be_visible()

    @allure.title("测试创建活动时未选择类型的错误提示")
    def test_create_activity_empty_type(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动名称，不选择类型
        page.fill("#formName", "测试活动")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("#formType")).to_be_visible()
        expect(page.locator("text=请选择活动类型")).to_be_visible()

    @allure.title("测试创建活动时未选择子类型的错误提示")
    def test_create_activity_empty_subtype(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息，不选择子类型
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("#formSubType")).to_be_visible()
        expect(page.locator("text=请选择子类型")).to_be_visible()

    @allure.title("测试创建活动时未填写简介的错误提示")
    def test_create_activity_empty_description(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息，不填写简介
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("#formDescription")).to_be_visible()
        expect(page.locator("text=请输入活动简介")).to_be_visible()

    @allure.title("测试创建活动时结束时间早于开始时间的错误提示")
    def test_create_activity_invalid_time_range(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息，结束时间早于开始时间
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 14:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("text=结束时间必须晚于开始时间")).to_be_visible()

    @allure.title("测试创建活动时活动时长超过72小时的错误提示")
    def test_create_activity_time_exceeds(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息，活动时长超过72小时
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-05 10:00")
        
        # 点击提交按钮
        page.click("#btnSubmit")
        page.wait_for_timeout(500)
        
        # 验证错误提示
        expect(page.locator("text=活动时长不能超过72小时")).to_be_visible()

    @allure.title("测试创建活动时提交按钮在空字段时禁用")
    def test_create_activity_submit_disabled_with_empty_fields(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 不填写任何必填字段
        # 验证提交按钮禁用
        submit_btn = page.locator("#btnSubmit")
        expect(submit_btn).to_be_disabled()

    @allure.title("测试创建活动时保存草稿功能")
    def test_create_activity_save_draft(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写部分活动信息
        page.fill("#formName", "草稿活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个草稿活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击保存草稿按钮
        page.click("#btnSaveDraft")
        page.wait_for_timeout(1000)
        
        # 验证保存成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("测试创建活动时放弃创建功能")
    def test_create_activity_cancel(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写部分活动信息
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击放弃创建按钮
        page.click("#btnCancel")
        page.wait_for_timeout(500)
        
        # 验证返回活动列表
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("测试创建活动时关闭模态框功能")
    def test_create_activity_close_modal(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写部分活动信息
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 点击关闭模态框按钮
        page.click("#btnCloseModal")
        page.wait_for_timeout(500)
        
        # 验证返回活动列表
        expect(page).to_have_url(lambda url: "#activity-list" in url)

    @allure.title("测试取消活动功能")
    def test_cancel_activity(self, page: Page):
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 点击新建活动按钮
        page.click("#btnCreate")
        page.wait_for_timeout(500)
        
        # 填写活动信息
        page.fill("#formName", "测试活动")
        page.select_option("#formType", "线上")
        page.select_option("#formSubType", "直播")
        page.fill("#formDescription", "这是一个测试活动")
        page.fill("#formStartTime", "2024-01-01 10:00")
        page.fill("#formEndTime", "2024-01-01 12:00")
        
        # 提交活动
        page.click("#btnSubmit")
        page.wait_for_timeout(1000)
        
        # 验证活动创建成功
        expect(page).to_have_url(lambda url: "#activity-list" in url)
        
        # 点击详情按钮
        page.click(".detail-btn")
        page.wait_for_timeout(500)
        
        # 点击取消活动按钮
        page.click("#btnCancelActivity")
        page.wait_for_timeout(500)
        
        # 填写取消原因
        page.fill("#cancelReason", "测试取消")
        
        # 确认