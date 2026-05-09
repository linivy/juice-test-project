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
}

# ==================== 活动管理项目配置 ====================
ACTIVITY_CONFIG = {
    "project_name": "活动管理系统",
    "base_url": "file:///C:/Users/ivy.wang/Desktop/juice-test-project/activity_management.html",
    "page_path": "/",
    "success_url": "#activity-list",
    
    # 页面没有独立登录，通过角色切换控制权限
    "has_login": False,
    "role_switch": "#roleSelect",
    
    "selectors": {
        "新建活动按钮": "#btnCreate",
        "活动名称": "#formName",
        "活动类型": "#formType",
        "活动子类型": "#formSubType",
        "其他活动类型": "#formOtherType",
        "开始时间": "#formStartTime",
        "结束时间": "#formEndTime",
        "活动简介": "#formDescription",
        "备注": "#formRemark",
        "线上平台": "#formOnlinePlatform",
        "省份": "#formProvince",
        "城市": "#formCity",
        "区县": "#formDistrict",
        "详细地址": "#formAddress",
        "保存草稿": "#btnSaveDraft",
        "完成创建": "#btnSubmit",
        "放弃创建": "#btnCancel",
        "关闭模态框": "#btnCloseModal",
        "详情按钮": ".detail-btn",
        "取消活动": "#btnCancelActivity",
        "确认取消": "#btnConfirmCancel",
        "取消原因": "#cancelReason",
        "角色切换": "#roleSelect",
    },
    
    "error_messages": {
        "empty_name": "请输入活动名称",
        "empty_type": "请选择活动类型",
        "empty_subtype": "请选择子类型",
        "empty_description": "请输入活动简介",
        "invalid_time_range": "结束时间必须晚于开始时间",
        "time_exceeds": "活动时长不能超过72小时",
    },
    
    "test_accounts": {
        "admin": {"role": "admin", "name": "管理员"},
        "user1": {"role": "user1", "name": "普通用户1"},
    },
}

def get_config(project: str = "juice"):
    """获取项目配置"""
    if project == "activity":
        return ACTIVITY_CONFIG
    return JUICE_CONFIG