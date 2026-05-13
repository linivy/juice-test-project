# test/ai/prompts.py
"""AI 提示词模板 - 支持代码完整性约束"""

# ==================== 项目上下文模板 ====================
PROJECT_CONTEXT_TEMPLATE = """
## 项目信息
- 项目名称：{project_name}
- 测试框架：pytest + playwright
- 基础URL：{base_url}
- 页面类型：{page_type}

## 页面结构说明
{page_structure}

## 操作流程
{operation_flow}

## 页面元素定位
{selectors_section}

## 断言规则
- 成功验证：URL 包含 {success_url}
- 失败验证：停留在 {page_path} 页面
- 错误消息：{error_messages_section}

## 有效测试账号
{accounts_section}
"""

# ==================== 通用测试点分类 ====================

FORM_PAGE_CATEGORIES = """
### 一、表单页面测试点

#### 1. 正向流程
- 填写所有必填字段，提交成功
- 提交成功后正确跳转/提示

#### 2. 必填字段校验
- 每个必填字段为空时，提示对应错误
- 多个必填字段同时为空时的处理

#### 3. 格式校验
- 邮箱格式不正确时提示错误
- 手机号格式不正确时提示错误
- 日期格式不正确时提示错误

#### 4. 边界值测试
- 字段最小长度
- 字段最大长度
- 超出最大长度时无法输入或提示
- 数值字段的最小值、最大值、边界外

#### 5. 级联/联动逻辑
- 选项A变化时，选项B的选项联动变化
- 选中特定选项时，额外显示/隐藏字段

#### 6. 时间/日期校验
- 不能选择过去时间
- 结束时间必须晚于开始时间
- 时长限制
- 跨天/跨月/闰年等特殊日期

#### 7. 文件上传
- 支持的文件格式
- 单个文件大小限制
- 总文件大小限制
- 文件数量限制
- 删除已选文件功能

#### 8. 富文本编辑器
- 加粗、斜体、下划线功能
- 居左、居中、居右对齐
- 插入超链接功能
- 字符数量限制

#### 9. 按钮操作
- 提交按钮在表单未完成时禁用
- 重置/放弃按钮清空表单
- 取消按钮返回上一页
- 重复快速点击提交只生效一次

#### 10. 安全测试
- SQL注入攻击防护
- XSS攻击防护
- 特殊字符处理
"""

LIST_PAGE_CATEGORIES = """
### 二、列表页面测试点

#### 1. 字段显示
- 所有配置的列正确显示
- 字段值超长时截断显示...
- 鼠标悬停显示完整内容
- 空数据显示占位符

#### 2. 搜索功能
- 按名称/关键词精确搜索
- 按名称/关键词模糊搜索
- 搜索无结果时显示空状态提示
- 搜索后重置搜索条件

#### 3. 筛选功能
- 单条件筛选
- 多条件组合筛选
- 同一筛选项多选
- 时间范围筛选
- 清除筛选条件

#### 4. 排序功能
- 默认按更新时间倒序
- 点击表头正序/倒序切换
- 支持按多个字段排序

#### 5. 分页功能
- 每页显示指定条数
- 上一页/下一页按钮
- 首页/末页按钮
- 跳转到指定页
- 分页后数据正确

#### 6. 导出功能
- 导出当前页数据
- 导出全部数据
- 导出格式验证
- 空数据导出提示

#### 7. 操作按钮
- 详情按钮跳转正确
- 编辑按钮权限控制
- 删除按钮确认弹框

#### 8. 数据权限
- Admin看到全部数据
- 普通用户只看到自己的数据
- 已删除数据不显示
"""

DETAIL_PAGE_CATEGORIES = """
### 三、详情页面测试点

#### 1. 字段显示
- 所有字段正确显示
- 富文本内容正确渲染
- 图片/文件可预览/下载
- 空字段显示占位符

#### 2. 数据一致性
- 详情数据与列表数据一致
- 修改后数据实时同步
- 操作历史记录完整

#### 3. 状态显示
- 状态标签颜色正确
- 状态文案正确
- 状态变化时实时更新

#### 4. 操作按钮（按状态显示）
- 待提交：显示编辑、删除
- 已发布：显示编辑、取消
- 已完成：不显示操作按钮
- 已取消：不显示操作按钮

#### 5. 编辑功能
- 点击编辑进入编辑模式
- 表单预填当前数据
- 编辑后保存成功
- 编辑后操作历史新增记录

#### 6. 取消/删除功能
- 取消操作需填写原因
- 确认弹框提示
- 成功后跳转列表页
- 操作历史记录取消原因

#### 7. 返回按钮
- 点击返回列表页
- 返回后列表数据正确
"""

SECURITY_CATEGORIES = """
### 四、安全测试点

#### 1. SQL注入
- 邮箱字段输入 SQL 注入 payload
- 搜索框输入 SQL 注入 payload
- 验证系统正确处理

#### 2. XSS攻击
- 输入框输入 XSS payload
- 富文本编辑器输入 XSS payload
- 验证输出被转义

#### 3. 越权操作
- 普通用户访问管理员页面
- 用户A编辑用户B的数据
- 用户A删除用户B的数据

#### 4. 重复提交
- 快速连续点击提交按钮
- 验证只提交一次

#### 5. 会话管理
- 会话超时后需重新登录
- 退出登录后无法访问受保护页面
"""
# ==================== 测试点生成提示词（优化版）====================

TEST_POINTS_PROMPT = """
你是资深测试架构师，擅长设计全面的测试用例。

{project_context}

## 需求信息
- 模块：{module_name}
- 功能：{feature_name}
- 需求：{requirement}

## 请按以下测试类型生成测试点

{test_categories}

## 编号规则
- TC-{module_name}-FUNC-XXX：正向流程
- TC-{module_name}-VALID-XXX：字段/格式校验
- TC-{module_name}-BOUND-XXX：边界值
- TC-{module_name}-CASCADE-XXX：级联逻辑
- TC-{module_name}-TIME-XXX：时间校验
- TC-{module_name}-FILE-XXX：文件上传
- TC-{module_name}-RICH-XXX：富文本
- TC-{module_name}-LIST-XXX：列表功能
- TC-{module_name}-DETAIL-XXX：详情功能
- TC-{module_name}-AUTH-XXX：权限控制
- TC-{module_name}-STATUS-XXX：状态流转
- TC-{module_name}-SEC-XXX：安全测试

## 输出格式
按优先级 P0/P1/P2 分组输出，每个测试点包含：
- 编号
- 测试描述
- 预期结果

## ⚠️ 完整性要求（必须遵守）
1. 必须覆盖上述【测试类型清单】中的每一种类型
2. 每个测试类型至少生成 2-3 个测试点
3. 如果输出内容较多，请优先完成当前分组后再继续
4. 不要在句子中间截断，确保每个测试点完整输出
5. 输出完成后，在末尾添加 [COMPLETE] 标记

不要添加额外解释，直接输出测试点列表。
"""

# ==================== 测试数据生成提示词 ====================

TEST_DATA_PROMPT = """
基于以下测试点，生成 pytest.param 格式的参数化测试数据：

{test_points}

输出格式：
test_data = [
    pytest.param("value1", "value2", {"success": True}, id="TC-001-描述"),
    pytest.param("", "value2", {"success": False, "error": "错误消息"}, id="TC-002-描述"),
]

要求：
- 每条数据包含 id 用于标识测试点
- 使用真实的有效测试数据
- 错误消息使用项目配置中的文案

## ⚠️ 完整性要求
1. 必须为每个测试点生成对应的测试数据
2. 确保每条测试数据完整（包含所有参数）
3. 输出完成后，在末尾添加 [COMPLETE] 标记

"""
# ==================== 代码生成提示词（核心优化版）====================

CODE_GENERATION_PROMPT = """
生成 pytest + playwright 测试代码。

{project_context}

## 测试点列表
{test_data}

## 模块信息
- 模块名称：{module_name}
- 功能名称：{feature_name}
- 页面路径：{page_path}

## 代码要求
1. 使用项目配置中的选择器定位元素
2. 包含辅助函数：close_dialog()、wait_for_toast()
3. 成功验证：URL 包含 success_url
4. 失败验证：停留在 page_path 并检查错误消息
5. 空字段时验证提交按钮禁用
6. 使用 allure 装饰器
7. 输出纯 Python 代码，不要额外解释
8. 🚨 不要使用 ```python 和 ``` 包裹代码，直接输出纯 Python 代码

## ⚠️ 代码完整性约束（最高优先级）
1. 每个测试方法必须有完整的函数体、闭合括号和至少一个断言
2. 不要在方法中间截断，如果无法完成所有测试点，请完成当前方法后停止
3. 确保所有括号、引号、方括号都已闭合
4. 每个测试方法都以 `def test_` 开头
5. 生成完成后，必须在最后一行添加 `[COMPLETE]` 标记
6. 🚨 禁止在代码开头添加 ```python，禁止在代码末尾添加 ```

## 代码模板（纯代码，不要包含反引号）
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "{{base_url}}"

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

@allure.feature("{{feature_name}}")
class Test{{module_name}}:

    @allure.title("测试用例")
    def test_example(self, page: Page):
        page.goto(f"{BASE_URL}{{page_path}}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        
        # 测试逻辑
        # ...
        expect(page).to_have_url(lambda url: "{{success_url}}" in url)

[COMPLETE]
"""

# ==================== 安全代码生成提示词（防截断版）====================

SAFE_CODE_GENERATION_PROMPT = """
生成 pytest + playwright 测试代码。

{project_context}

## 当前批次测试点（共 {batch_count} 个）
{batch_points}

## 模块信息
- 模块名称：{module_name}
- 功能名称：{feature_name}
- 当前批次号：{batch_num}/{total_batches}
- 基础URL：{base_url}
- 页面路径：{page_path}
- 成功URL：{success_url}

## 代码要求
1. 为每个测试点生成一个独立的测试方法
2. 每个测试方法至少包含 3-5 个操作步骤和 1 个断言
3. 使用项目配置中的选择器定位元素
4. 包含辅助函数：close_dialog()、wait_for_toast()
5. 使用 @allure.feature 和 @allure.title 装饰器
6. 🚨 不要使用 ```python 和 ``` 包裹代码，直接输出纯 Python 代码

## 🚨 防截断规则（必须严格遵守）
1. 完整优先原则：宁可少生成几个完整的测试方法，也不要生成半个不完整的方法
2. 强制结束标记：生成完成后必须输出 [COMPLETE]
3. 括号检查：每个 ( 必须有对应的 )
4. 断言完整：每个 expect( 必须以 ) 结束
5. 方法边界：每个方法结束后确认闭合
6. 🚨 禁止在代码开头添加 ```python，禁止在代码末尾添加 ```

## 🚨 导入规则
1. **禁止**导入不存在的模块如 `from conftest import page`
2. **不要**导入 `page`，`page` 是 pytest 的 fixture，由 pytest 自动注入
3. **只允许**导入以下模块：`pytest`, `allure`, `playwright.sync_api`, `datetime`, `time`, `os`
4. **不要**使用 `from config import selectors` 这种导入方式，请直接使用硬编码的选择器

## 代码模板（纯代码，不要包含反引号）
import pytest
from playwright.sync_api import Page, expect
import allure

BASE_URL = "{base_url}"

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

@allure.feature("{feature_name}")
class Test{module_name}:

    @allure.title("TC-XXX: 测试描述")
    def test_example(self, page: Page):
        page.goto(f"{BASE_URL}{page_path}")
        page.wait_for_load_state("networkidle")
        close_dialog(page)
        expect(page).to_have_url(lambda url: "{success_url}" in url)

[COMPLETE]
"""

# ==================== 修复截断代码的提示词 ====================

FIX_TRUNCATION_PROMPT = """
以下代码被截断了，请修复并补全：
## 修复要求
1. 补全所有未闭合的括号
2. 补全所有未闭合的引号
3. 补全被截断的 assert/expect 语句
4. 确保每个测试方法完整
5. 输出完整的代码

```python
{truncated_code}
```
[COMPLETE]
"""
# ==================== 工具函数 ====================

def build_project_context(config: dict) -> str:
    """根据项目配置构建上下文"""
    
    page_type = config.get("page_type", "multi_page")
    base_url = config.get("base_url", "待填写")
    success_url = config.get("success_url", "待填写")
    page_path = config.get("page_path", "待填写")
    has_login = config.get("has_login", True)
    selectors = config.get("selectors", {})
    
    # 获取关键选择器
    role_switch = selectors.get("角色切换", "#roleSelect")
    create_btn = selectors.get("新建活动按钮", "#btnCreate")
    submit_btn = selectors.get("完成创建", "#btnSubmit")
    save_draft_btn = selectors.get("保存草稿", "#btnSaveDraft")
    
    # 构建页面结构说明
    if not has_login:
        page_structure = "- 单页面应用，无需登录\n- 使用角色切换测试权限"
        operation_flow = f"1. 访问 {base_url}\n2. 切换角色: {role_switch}\n3. 点击: {create_btn}\n4. 提交: {submit_btn}"
    else:
        page_structure = "- 多页面应用，需要登录"
        operation_flow = "1. 登录\n2. 访问功能页面"
    
    return PROJECT_CONTEXT_TEMPLATE.format(
        project_name=config.get("project_name", "未知项目"),
        base_url=base_url,
        page_type="单页面应用" if not has_login else "多页面应用",
        page_structure=page_structure,
        operation_flow=operation_flow,
        selectors_section="- 请参考 config.py 中的 selectors 配置",
        success_url=success_url,
        page_path=page_path,
        error_messages_section="- 请参考 config.py 中的 error_messages 配置",
        accounts_section="- 请参考 config.py 中的 test_accounts 配置",
    )

def get_test_categories(page_type: str = "all") -> str:
    """根据页面类型获取测试分类"""
    categories = []
    
    if page_type in ["form", "all"]:
        categories.append(FORM_PAGE_CATEGORIES)
    if page_type in ["list", "all"]:
        categories.append(LIST_PAGE_CATEGORIES)
    if page_type in ["detail", "all"]:
        categories.append(DETAIL_PAGE_CATEGORIES)
    if page_type in ["security", "all"]:
        categories.append(SECURITY_CATEGORIES)
    
    return "\n".join(categories)

def get_batch_generation_prompt(
    project_context: str,
    batch_points: list,
    module_name: str,
    feature_name: str,
    batch_num: int,
    total_batches: int,
    base_url: str,
    page_path: str,
    success_url: str
) -> str:
    """构建批次生成提示词"""
    
    batch_text = "\n".join([f"- {point}" for point in batch_points])
    
    return SAFE_CODE_GENERATION_PROMPT.format(
        project_context=project_context,
        batch_count=len(batch_points),
        batch_points=batch_text,
        module_name=module_name,
        feature_name=feature_name,
        batch_num=batch_num,
        total_batches=total_batches,
        base_url=base_url,
        page_path=page_path,
        success_url=success_url,
    )

def get_fix_truncation_prompt(truncated_code: str) -> str:
    """构建修复截断代码的提示词"""
    return FIX_TRUNCATION_PROMPT.format(truncated_code=truncated_code)

# ==================== 导出列表 ====================

__all__ = [
    # 模板
    'PROJECT_CONTEXT_TEMPLATE',
    'FORM_PAGE_CATEGORIES',
    'LIST_PAGE_CATEGORIES',
    'DETAIL_PAGE_CATEGORIES',
    'SECURITY_CATEGORIES',
    
    # 提示词
    'TEST_POINTS_PROMPT',
    'TEST_DATA_PROMPT',
    'CODE_GENERATION_PROMPT',
    'SAFE_CODE_GENERATION_PROMPT',
    'FIX_TRUNCATION_PROMPT',
    
    # 工具函数
    'build_project_context',
    'get_test_categories',
    'get_batch_generation_prompt',
    'get_fix_truncation_prompt',
]