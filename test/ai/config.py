# test/ai/config.py
"""项目配置 - 根据具体项目修改"""

# ==================== Juice Shop 项目配置 ====================
JUICE_CONFIG = {
    "project_name": "Juice Shop",
    "base_url": "http://localhost:3000",
    "page_path": "/#/login",
    "success_url": "/#/search",
    
    "selectors": {
        "email": "#email",
        "password": "#password",
        "login_button": "#loginButton",
    },
    
    "error_messages": {
        "empty_email": "Email is required",
        "empty_password": "Password is required",
        "invalid_credentials": "Invalid email or password",
        "email_format": "Please enter a valid email address",
    },
    
    "test_accounts": {
        "admin": {"email": "admin@juice-sh.op", "password": "admin123"},
        "user": {"email": "jim@juice-sh.op", "password": "ncc-1701"},
    },
    
    "generation": {
        "max_tokens_per_batch": 6000,
        "safe_tokens_buffer": 1500,
        "default_batch_size": 8,
        "max_test_steps": 25,
        "enable_completeness_check": True,
        "enable_auto_fix": True,
        "max_retries": 2,
    },
}


# ==================== 活动管理项目配置 ====================
ACTIVITY_CONFIG = {
    # ==================== 基础配置 ====================
    "project_name": "activity",
    "base_url": "http://localhost:5000",
    "page_path": "/",
    "success_url": "#activity-list",
    "has_login": False,
    "role_switch": "#roleSelect",
    
    # ==================== 选择器配置 ====================
    "selectors": {
        # 按钮
        "btn_create": "#btnCreate",
        "btn_submit": "#btnSubmit",
        "btn_save_draft": "#btnSaveDraft",
        "btn_cancel": "#btnCancel",
        "btn_confirm": "#btnConfirm",
        "btn_confirm_cancel": "#btnConfirmCancel",
        "btn_close_modal": "#btnCloseModal",
        
        # 表单字段
        "form_name": "#formName",
        "form_type": "#formType",
        "form_sub_type": "#formSubType",
        "form_other_type": "#formOtherType",
        "form_start_time": "#formStartTime",
        "form_end_time": "#formEndTime",
        "form_description": "#formDescription",
        "form_remark": "#formRemark",
        "form_online_platform": "#formOnlinePlatform",
        
        # 地址相关
        "form_province": "#formProvince",
        "form_city": "#formCity",
        "form_district": "#formDistrict",
        "form_address": "#formAddress",
        
        # 地点选择（radio）
        "location_online": "input[name='locationType'][value='online']",
        "location_offline": "input[name='locationType'][value='offline']",
        
        # 文件上传
        "file_input": "#fileInput",
        "upload_area": "#uploadArea",
        
        # 模态框
        "create_modal": "#createModal",
        "confirm_modal": "#confirmModal",
        "cancel_modal": "#cancelModal",
        
        # 其他
        "toast": "#toast",
        "activity_list": "#activityTableBody",
        "role_select": "#roleSelect",
    },
    
    # ==================== 错误消息配置 ====================
    "error_messages": {
        "empty_name": "请输入活动名称",
        "empty_type": "请选择活动类型",
        "empty_subtype": "请选择子类型",
        "empty_description": "请输入活动简介",
        "empty_start_time": "请选择开始时间",
        "empty_end_time": "请选择结束时间",
        "invalid_time_range": "结束时间必须晚于开始时间",
        "time_exceeds": "活动时长不能超过72小时",
        "type_disabled": "所选活动类型已被停用，请选择新的活动类型",
        "file_format_error": "文件格式错误",
        "file_size_error": "文件大小超过限制",
        "char_limit": "字符超限",
    },
    
    # ==================== 成功消息配置 ====================
    "success_messages": {
        "create_success": "活动创建成功",
        "save_draft": "草稿已保存",
        "save_draft_detail": "草稿已保存，稍后可以继续编辑",
        "cancel_success": "活动已取消",
        "delete_success": "已删除",
    },
    
    # ==================== 级联选项配置 ====================
    "cascade_options": {
        "formType": {
            "社区活动": {
                "value": "community",
                "sub_options": ["运动会", "知识讲座", "才艺比赛"],
                "wait_selector": "#subTypeDiv"
            },
            "家庭活动": {
                "value": "family",
                "sub_options": ["亲子活动", "户外露营", "亲子烘培"],
                "wait_selector": "#subTypeDiv"
            },
            "其他": {
                "value": "other",
                "sub_options": [],
                "show_selector": "#formOtherType",
                "hide_selector": "#subTypeDiv"
            }
        }
    },
    
    # ==================== 地点模式配置 ====================
    "location_modes": {
        "online": {
            "trigger_selector": "input[name='locationType'][value='online']",
            "visible_fields": ["#formOnlinePlatform"],
            "hidden_fields": ["#formProvince", "#formCity", "#formDistrict", "#formAddress"]
        },
        "offline": {
            "trigger_selector": "input[name='locationType'][value='offline']",
            "visible_fields": ["#formProvince", "#formCity", "#formDistrict", "#formAddress"],
            "hidden_fields": ["#formOnlinePlatform"]
        }
    },
    
    # ==================== 级联选择规则 ====================
    "cascade_rules": {
        "province_city": {
            "parent": "#formProvince",
            "child": "#formCity",
            "wait_condition": "#formCity option[value!='']",
            "description": "选择省份后城市选项才会加载"
        },
        "city_district": {
            "parent": "#formCity",
            "child": "#formDistrict",
            "wait_condition": "#formDistrict option[value!='']",
            "description": "选择城市后区县选项才会加载"
        }
    },
    
    # ==================== 验证规则 ====================
    "validation_rules": {
        "required_fields_for_submit": ["form_name", "form_type", "form_start_time", "form_end_time", "form_description"],
        "required_fields_for_draft": ["form_name", "form_type"],
        "field_limits": {
            "form_name": 50,
            "form_description": 500,
            "form_online_platform": 50,
            "form_address": 50,
            "form_other_type": 50,
        }
    },
    
    # ==================== 辅助函数 ====================
    "helper_functions": """
    def wait_for_cascade_load(page, child_selector, timeout=5000):
        '''等待级联下拉框选项加载'''
        page.wait_for_selector(f"{child_selector} option[value!='']", state="visible", timeout=timeout)

    def select_province_city_district(page, province, city, district):
        '''选择省市区'''
        page.select_option("#formProvince", province)
        wait_for_cascade_load(page, "#formCity")
        page.select_option("#formCity", city)
        wait_for_cascade_load(page, "#formDistrict")
        page.select_option("#formDistrict", district)

    def fill_required_fields_for_draft(page, name, activity_type):
        '''填写草稿必填字段'''
        page.fill("#formName", name)
        page.select_option("#formType", activity_type)
        # 如果是社区活动或家庭活动，需要等待子类型下拉框
        if activity_type in ["社区活动", "家庭活动"]:
            page.wait_for_selector("#subTypeDiv", state="visible")
            page.select_option("#formSubType", "运动会")  # 示例值
    """,

    "generation": {
        "max_tokens_per_batch": 6000,
        "safe_tokens_buffer": 1500,
        "default_batch_size": 8,
        "max_test_steps": 25,
        "enable_completeness_check": True,
        "enable_auto_fix": True,
        "max_retries": 2,
        "renumber_tests": True,
    },
}

def get_config(project: str = "juice"):
    """获取项目配置"""
    if project == "activity":
        return ACTIVITY_CONFIG
    return JUICE_CONFIG


def get_generation_config(project: str = "juice"):
    """获取代码生成安全配置"""
    config = get_config(project)
    return config.get("generation", {
        "max_tokens_per_batch": 6000,
        "safe_tokens_buffer": 1500,
        "default_batch_size": 8,
        "max_test_steps": 25,
        "enable_completeness_check": True,
        "enable_auto_fix": True,
        "max_retries": 2,
    })


def get_location_mode_hint(project: str = "activity") -> str:
    """获取地点模式相关的提示词"""
    config = get_config(project)
    modes = config.get("location_modes", {})  # 改为 location_modes
    
    if not modes:
        return ""
    
    hint = """
## 📍 地点模式说明（⚠️ 重要）

根据不同的地点选择，需要操作不同的表单字段：

### 线上模式
- ✅ 正确：`page.click('input[name="locationType"][value="online"]')`
- 需要操作的字段：`#formOnlinePlatform`
- **不要操作**：`#formProvince`, `#formCity`, `#formDistrict`, `#formAddress`

### 线下模式
- ✅ 正确：`page.click('input[name="locationType"][value="offline"]')`
- 需要操作的字段：`#formProvince`, `#formCity`, `#formDistrict`, `#formAddress`
- **不要操作**：`#formOnlinePlatform`

### 示例代码
```python
# 线上模式示例
page.click('input[name="locationType"][value="online"]')
page.fill("#formOnlinePlatform", "腾讯会议")

# 线下模式示例
page.click('input[name="locationType"][value="offline"]')
page.select_option("#formProvince", "广东省")
page.select_option("#formCity", "深圳市")
page.select_option("#formDistrict", "南山区")
page.fill("#formAddress", "科技园南区A栋")

"""
    return hint

def get_cascade_hint(project: str = "activity") -> str:
    """获取级联联动相关的提示词"""
    config = get_config(project)
    cascade = config.get("cascade_options", {})
    form_type = cascade.get("formType", {})
    
    if not form_type:
        return ""
    
    hint = """
## 🔗 级联联动说明（重要！）

活动类型 `#formType` 选择后会影响二级下拉框 `#formSubType` 的选项：

"""
    for opt_name, opt_config in form_type.items():
        sub_opts = opt_config.get("sub_options", [])
        show_selector = opt_config.get("show_selector", "")
        hide_selector = opt_config.get("hide_selector", "")
        
        if sub_opts:
            hint += f"- 选择 **{opt_name}** 后：二级下拉框显示 {', '.join(sub_opts)}\n"
        elif show_selector:
            hint += f"- 选择 **{opt_name}** 后：二级下拉框消失，显示 `#formOtherType` 输入框\n"
    
    hint += """
### 操作步骤：

#### 普通级联（社区活动/家庭活动）：
```python
# 1. 选择活动类型
page.select_option("#formType", "社区活动")
# 2. 等待二级下拉框出现
page.wait_for_selector("#subTypeDiv", state="visible")
# 3. 选择二级类型
page.select_option("#formSubType", "运动会")
```
#### 特殊级联（其他）：
```python
# 1. 选择活动类型为"其他"
page.select_option("#formType", "其他")
# 2. 等待二级下拉框消失
page.wait_for_selector("#subTypeDiv", state="hidden")
# 3. 填写活动类型说明
page.fill("#formOtherType", "这是一个自定义活动类型说明")
```
### 注意事项：
- 操作 `#formSubType` 前，**必须先选择** `#formType` 并等待元素出现
- 选择"其他"时，`#formSubType` 会隐藏，需要操作 `#formOtherType`
"""
    return hint


def get_all_hints(project: str = "activity") -> str:
    """获取所有增强提示词"""
    hints = []
    
    location_hint = get_location_mode_hint(project)
    if location_hint:
        hints.append(location_hint)
    
    cascade_hint = get_cascade_hint(project)
    if cascade_hint:
        hints.append(cascade_hint)
    
    return "\n".join(hints)
