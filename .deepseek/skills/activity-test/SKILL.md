---
name: activity-test
description: Use when generating pytest+Playwright test cases for the 活动管理 (Activity Management) system. Triggered by tasks mentioning Requirements/ activity docs, writing/modifying tests under test/ai/generated/activity/, or debugging Playwright selectors for activity_management.html. Also triggered when the user asks to "generate test cases", "write tests", or "create automation tests" for the activity module.
---

# Activity Management Test Generator

Generate standalone, runnable pytest + Playwright test files for the Activity
Management SPA (`demo/activity_management.html`). Tests are placed under
`test/ai/generated/activity/`.

---

## 1. 能力范围

This skill covers:

- **需求分析** — Parse `Requirements/活动管理_*.md` to extract test points
- **选择器映射** — Map requirement fields to DOM selectors via `config/activity.yaml`
- **代码生成** — Produce test files following the project conventions described below
- **代码修复** — Diagnose and fix failing tests (selector typos, missing waits, cascade timing)

This skill does NOT cover:

- Modifying the AI generation pipeline itself (`test/ai/test_generator.py` etc.)
- Modifying the demo application (`demo/` files)
- General Playwright or pytest tutorials

---

## 2. 文件引用规范

Load files on demand, not all at once. Reference priority:

| # | File | When to open | What to extract |
|---|------|-------------|-----------------|
| 1 | `config/activity.yaml` | Always — first read. Maps requirements to selectors | selectors, error_messages, cascade_options, location_modes, success_messages, validation_rules, selector_aliases, error_element_mapping |
| 2 | `Requirements/活动管理_{NN}_{模块}.md` | Parse user-mentioned feature or module name | Test cases (TC-* IDs, descriptions, expected results), priority levels |
| 3 | `Requirements/活动管理.md` | Need field definitions, button behaviors, or permission rules | Full field table, button semantics, status definitions |
| 4 | `demo/activity_management.html` | Need exact DOM selectors or JS behavior not in activity.yaml | Element IDs, data-* attributes, event handlers, show/hide logic |
| 5 | `test/ai/generated/activity/conftest.py` | Writing or modifying test files — import available helpers | helper function signatures and imports |
| 6 | `test/ai/generated/activity/test_create_activity.py` | Need reference patterns for test class/method style | Import style, class/method naming, assertion patterns, docstring format |

**Rule:** Never load all 6 at once. Start with (1), then (2), then only the
specific sections of (3)(4) needed. Use (5) and (6) as style references only.

---

## 3. 需求文档解析规则

### 3.1 文档结构识别

需求文档使用以下层级结构：

```markdown
# 活动管理 - {功能模块名称}模块

## 测试点

### P{0|1|2} - {场景分类}

- TC-{MODULE}-{INDEX}-{NNN}: {中文测试描述}
  预期结果：{可验证的预期结果}
```

### 3.2 TC ID 解析

格式：`TC-{MODULE_ABBR}-{NNN}`

模块缩写映射表：

| 需求文件 | 模块缩写 | 示例 TC ID |
|---------|---------|------------|
| 活动管理_01_创建活动 | CREATE | TC-ACTIVITY-CREATE-001 |
| 活动管理_02_活动列表 | LIST | TC-ACTIVITY-LIST-001 |
| 活动管理_03_活动详情 | DETAIL | TC-ACTIVITY-DETAIL-001 |
| 活动管理_04_编辑活动 | EDIT | TC-ACTIVITY-EDIT-001 |
| 活动管理_05_取消活动 | CANCEL | TC-ACTIVITY-CANCEL-001 |
| 活动管理_06_删除活动 | DELETE | TC-ACTIVITY-DELETE-001 |
| 活动管理_07_状态流转 | STATUS | TC-ACTIVITY-STATUS-001 |
| 活动管理_08_边界值与校验 | VALID | TC-ACTIVITY-VALID-001 |
| 活动管理_09_文件上传 | FILE | TC-ACTIVITY-FILE-001 |
| 活动管理_10_富文本编辑器 | RICH | TC-ACTIVITY-RICH-001 |
| 活动管理_11_安全测试 | SEC | TC-ACTIVITY-SEC-001 |

### 3.3 预期结果 → 断言映射

从 `预期结果` 文本生成断言：

| 预期结果关键词 | 断言类型 |
|-------------|---------|
| "弹出"、"弹框" | `expect(page.locator("#{modalId}.show")).to_be_visible()` |
| "toast"、"显示"{msg} | `assert get_toast_text(page)` + `expect(toast).to_contain_text(msg)` |
| "错误"、"{字段}显示"{msg} | `get_error_text(page, fieldId)` + `assert msg in error_text` |
| "跳转"、"返回" | `expect(listPage).to_be_visible()` 或 URL 检查 |
| "隐藏"、"消失" | `expect(locator).to_be_hidden()` |
| "可见"、"显示"（非弹框） | `expect(locator).to_be_visible()` |
| "状态"、"变为" | 文本内容断言 |
| "历史记录"、"包含" | `expect(table).to_contain_text(...)` |

---

## 4. 选择器使用规范

### 4.1 选择器来源

所有选择器来自 `config/activity.yaml` 的以下配置段：

- `selectors:` → 主选择器映射
- `selector_aliases:` → 别名映射（用于自动修复脚本，测试代码不直接使用别名）
- `error_element_mapping:` → 字段 → 错误元素映射

### 4.2 表单字段选择器速查

```
字段类型            →  选择器                  →  Playwright 操作
─────────────────────────────────────────────────────────────────
活动名称 (必填)     →  #formName               →  page.fill()
活动类型 (必填)     →  #formType               →  page.select_option() 值: community|family|other
子类型              →  #formSubType             →  page.select_option() (先等待 #subTypeDiv 可见)
其他类型说明        →  #formOtherType           →  page.fill() (仅 #formType=other 时可见)
开始时间 (必填)     →  #formStartTime           →  page.evaluate() 通过 _flatpickr.setDate()
结束时间 (必填)     →  #formEndTime             →  page.evaluate() 通过 _flatpickr.setDate()
活动简介 (必填)     →  #formDescription         →  page.evaluate() 设置 innerHTML (contenteditable div)
备注                →  #formRemark              →  page.fill()
平台名称            →  #formOnlinePlatform      →  page.fill() (仅线上时可见)
省份                →  #formProvince            →  page.select_option() (级联 → City → District)
城市                →  #formCity                →  page.select_option()
区县                →  #formDistrict            →  page.select_option()
详细地址            →  #formAddress             →  page.fill() (仅线下时可见)
文件上传            →  #fileInput               →  page.set_input_files()
```

### 4.3 按钮选择器

```
按钮         →  选择器               →  说明
──────────────────────────────────────────────────
新建活动     →  #btnCreate           →  打开创建弹窗
完成创建     →  #btnSubmit           →  提交表单
保存草稿     →  #btnSaveDraft        →  保存为待提交
放弃创建     →  #btnCancel           →  触发放弃确认
确认弹框-确定 →  #btnConfirm          →  在 #confirmModal 内
确认弹框-取消 →  #btnConfirmCancelBtn →  在 #confirmModal 内
```

### 4.4 弹窗和提示选择器

```
元素           →  选择器           →  可见性检测
───────────────────────────────────────────────────
创建弹窗       →  #createModal     →  .show class
确认弹窗       →  #confirmModal    →  .show class
取消弹窗       →  #cancelModal     →  .show class
Toast 提示     →  #toast           →  wait_for(state="visible")
子类型容器     →  #subTypeDiv      →  style display 切换
线上字段容器   →  #onlineLocation  →  style display 切换
线下字段容器   →  #offlineLocation →  style display 切换
列表表格体     →  #activityTableBody
角色切换       →  #roleSelect      →  值为 admin | user1
```

### 4.5 错误消息选择器

错误消息元素遵循模式 `#error_{fieldId}`：

```
formName        →  #error_formName
formType        →  #error_formType
formSubType     →  #error_formSubType
formStartTime   →  #error_formStartTime
formEndTime     →  #error_formEndTime
formDescription →  #error_formDescription
```

错误消息内容在 `config/activity.yaml` → `error_messages:` 段定义。

---

## 5. 代码生成模板

### 5.1 文件头模板

```python
# test/ai/generated/activity/test_{feature_lower}.py
"""{模块中文名} - {功能中文名}模块自动化测试

基于需求文档: Requirements/{需求文件名}.md
测试框架: Playwright + pytest
前端: demo/activity_management.html
"""

import pytest
from playwright.sync_api import Page, expect

from test.ai.generated.activity.conftest import (
    {按需导入的 helper 函数列表}
)
```

### 5.2 测试类模板

```python
# ==================== P{0|1|2}: {场景中文分类} ====================


class Test{ModuleName}{ScenarioName}:
    """P{0|1|2} - {场景中文描述}"""

    def test_{feature}_{scenario_detail}(self, {fixture_name}: Page):
        """TC-ACTIVITY-{MODULE}-{NNN}: {需求文档中的中文测试描述}"""
        page = {fixture_name}

        # 1. {第一步中文描述}
        {操作步骤}

        # {N}. {最后一步}
        {断言}
```

### 5.3 命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 文件名 | `test_{module_lower}.py` | `test_create_activity.py` |
| 类名 | `Test{模块}{场景}` PascalCase | `TestCreateActivityValidation` |
| 方法名 | `test_{动作}_{对象}` snake_case | `test_name_empty_others_valid` |
| 方法 docstring | 第一行写 TC ID + 完整中文描述 | `"""TC-ACTIVITY-CREATE-005: 仅活动名称为空..."""` |
| 步骤注释 | `# {序号}. {中文描述}` | `# 1. 填写活动名称` |
| 断言消息 | `f"期望{预期}，实际: {实际}"` | `f"期望 toast 包含'成功'，实际: {toast_text}"` |

### 5.4 导入规范

从 `test.ai.generated.activity.conftest` 导入的 helper 必须逐个显式列出，不使用 `*`：

```python
from test.ai.generated.activity.conftest import (
    BASE_URL,
    set_flatpickr_date,
    set_rich_text,
    fill_form_name,
    # ... 只导入实际使用的
)
```

`Page` 和 `expect` 从 `playwright.sync_api` 导入，不通过 conftest 转发。

### 5.5 断言模式选择

```
检查元素可见  →  expect(locator).to_be_visible()
检查元素隐藏  →  expect(locator).to_be_hidden()
检查文本内容  →  assert "text" in locator.inner_text()
检查输入值    →  assert page.input_value("#id") == "expected"
检查 Toast    →  get_toast_text(page) 后 assert ... in ...
检查错误消息  →  get_error_text(page, "fieldName") 后 assert ... in ...
检查弹窗可见  →  is_modal_visible(page, "modalId") 返回 bool
```

---

## 6. 特殊处理规则

### 6.1 富文本编辑器 (contenteditable)

`#formDescription` 是 `<div contenteditable="true">`，不能用 `page.fill()`。

```python
# 正确做法 — 通过 evaluate 设置 innerHTML
page.evaluate(
    """([sel, html]) => {
        const el = document.querySelector(sel);
        if (el) {
            el.innerHTML = html;
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }""",
    ["#formDescription", "<p>活动简介内容</p>"],
)
```

> conftest.py 已提供 `set_rich_text(page, selector, html_content)` 封装此逻辑。

### 6.2 日期选择器 (flatpickr)

`#formStartTime` 和 `#formEndTime` 被 flatpickr 接管，`page.fill()` 无效。

```python
# 正确做法 — 通过 flatpickr 实例 API 设置
page.locator("#formStartTime").click()
page.wait_for_timeout(300)

page.evaluate(
    """([sel, date]) => {
        const el = document.querySelector(sel);
        if (el && el._flatpickr) {
            el._flatpickr.setDate(date);
        }
    }""",
    ["#formStartTime", "2026-06-20 09:00"],
)

page.keyboard.press("Escape")  # 关闭弹出的日历面板
page.wait_for_timeout(200)
```

**日期格式：** `YYYY-MM-DD HH:MM`（与 flatpickr 配置 `dateFormat: "Y-m-d H:i"` 一致）。

**约束：** flatpickr 设置了 `minDate: "today"`，开始时间不可选过去日期。测试中应选择未来日期。

> conftest.py 已提供 `set_flatpickr_date(page, selector, date_str)` 封装此逻辑。

### 6.3 活动类型级联

```
选择 community  →  #subTypeDiv 显示  →  #formSubType 选项: 运动会/知识讲座/才艺比赛
选择 family     →  #subTypeDiv 显示  →  #formSubType 选项: 亲子活动/户外露营/亲子烘焙
选择 other      →  #subTypeDiv 隐藏  →  #formOtherType 显示 (必填，限50字符)
```

操作序列：

```python
# community / family
page.select_option("#formType", "community")
page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
page.select_option("#formSubType", "运动会")

# other
page.select_option("#formType", "other")
page.wait_for_timeout(300)
# #subTypeDiv 应隐藏
expect(page.locator("#subTypeDiv")).to_be_hidden()
# #formOtherType 应可见
page.fill("#formOtherType", "自定义活动类型")
```

### 6.4 地点模式切换

```
线上 →  input[name='locationType'][value='online']  →  #onlineLocation 显示, #offlineLocation 隐藏
线下 →  input[name='locationType'][value='offline'] →  #offlineLocation 显示, #onlineLocation 隐藏
```

```python
# 线上
page.check("input[name='locationType'][value='online']")
page.wait_for_timeout(300)
page.fill("#formOnlinePlatform", "腾讯会议")

# 线下 (含省市区三级级联)
page.check("input[name='locationType'][value='offline']")
page.wait_for_timeout(300)
page.select_option("#formProvince", "广东省")
page.wait_for_timeout(500)   # 等待城市 API 加载
page.select_option("#formCity", "深圳市")
page.wait_for_timeout(500)   # 等待区县 API 加载
page.select_option("#formDistrict", "南山区")
page.fill("#formAddress", "科技园南区A栋")
```

> conftest.py 已提供 `select_location_online/offline()` 和 `fill_offline_address()` 封装。

### 6.5 弹框交互

三种弹框及其确认/取消按钮：

| 弹框 | 触发方式 | 确定按钮 | 取消/关闭按钮 |
|------|---------|---------|-------------|
| #createModal | 点击 #btnCreate | #btnSubmit (完成创建) / #btnSaveDraft (保存草稿) | #btnCancel (放弃创建) |
| #confirmModal | 提交或放弃时自动弹出 | #btnConfirm | #btnConfirmCancelBtn |
| #cancelModal | 取消活动时触发 | #btnConfirmCancel | #btnCloseCancelModal |

**确认弹框互动模式：**

```python
# 提交 → 确认
page.click("#btnSubmit")
page.wait_for_selector("#confirmModal.show", timeout=5000)
page.click("#btnConfirm")          # 确认
page.wait_for_timeout(300)

# 放弃 → 确认放弃
page.click("#btnCancel")
page.wait_for_selector("#confirmModal.show", timeout=5000)
page.click("#btnConfirm")          # 确认放弃，返回列表页

# 放弃 → 取消放弃
page.click("#btnCancel")
page.wait_for_selector("#confirmModal.show", timeout=5000)
page.click("#btnConfirmCancelBtn") # 取消，停留在表单
```

### 6.6 Toast 验证

```python
toast = page.locator("#toast")
toast.wait_for(state="visible", timeout=5000)
toast_text = toast.inner_text()
assert "活动创建成功" in toast_text
```

> conftest.py 已提供 `get_toast_text(page)` 封装。

---

## 7. 工具函数库 (conftest.py)

以下是 `test/ai/generated/activity/conftest.py` 中可用的 fixtures 和函数。新生成的测试文件应优先使用这些，避免重复定义。

### 7.1 Fixtures

| Fixture | 作用域 | 用途 |
|---------|-------|------|
| `activity_page` | function | 打开 http://localhost:5000 → 等待 #listPage 可见 → 返回 page |
| `create_modal_open` | function | 基于 activity_page，再点击 #btnCreate → 等待 #createModal.show → 返回 page |
| `browser_context_args` | session | 设置 viewport 1280×720 |

### 7.2 表单操作函数

```python
fill_form_name(page, name: str)               # page.fill("#formName", name)
select_activity_type(page, type_value: str)    # page.select_option("#formType", type_value) + wait 300ms
  # type_value: "community" | "family" | "other"
select_sub_type(page, sub_type: str)           # page.select_option("#formSubType", sub_type) + wait 200ms
select_location_online(page)                   # page.check("input[name='locationType'][value='online']") + wait 300ms
select_location_offline(page)                  # page.check("input[name='locationType'][value='offline']") + wait 300ms
fill_offline_address(page, province, city, district, address)  # 4 步操作 + 级联等待
clear_form_name(page)                          # page.fill("#formName", "")
clear_activity_type(page)                      # page.select_option("#formType", "") + wait 200ms
upload_attachment(page, file_path: str)        # page.set_input_files("#fileInput", file_path) + wait 500ms
```

### 7.3 特殊元素操作函数

```python
set_flatpickr_date(page, selector: str, date_str: str)
  # 通过 page.evaluate() 调用 el._flatpickr.setDate()
  # selector: "#formStartTime" 或 "#formEndTime"
  # date_str: "2026-06-20 09:00"

set_rich_text(page, selector: str, html_content: str)
  # 通过 page.evaluate() 设置 innerHTML + dispatch input event
  # selector: "#formDescription"
  # html_content: "<p>活动简介</p>"
```

### 7.4 按钮操作函数

```python
submit_create(page)        # page.click("#btnSubmit")
save_draft(page)           # page.click("#btnSaveDraft")
discard_create(page)       # page.click("#btnCancel")
confirm_modal(page)        # page.click("#confirmModal #btnConfirm") + wait 300ms
cancel_modal_close(page)   # page.click("#btnConfirmCancelBtn") + wait 300ms
```

### 7.5 断言辅助函数

```python
get_toast_text(page) -> str
  # 等待 toast 可见 → 返回 inner_text()

get_error_text(page, field_id: str) -> str
  # 拼接 "#error_{field_id}" 选择器 → 可见时返回 inner_text()，不可见返回 ""

is_modal_visible(page, modal_id: str) -> bool
  # 检查 "#{modal_id}.show" 是否存在
```

### 7.6 不使用 helper 函数的情况

当现有 helper 无法覆盖时（如操作列表页、详情页），直接在测试方法中操作：
- 选择器从 `config/activity.yaml` 查找
- 操作后适当等待（`page.wait_for_timeout(300-500)` 用于 UI 动画）
- 添加中文注释说明操作意图

---

## 8. 断言和错误消息规范

### 8.1 预期的错误消息

从 `config/activity.yaml` → `error_messages:` 获取：

| 场景 | 预期消息 | 触发条件 |
|------|---------|---------|
| 活动名称为空 | `请输入活动名称` | #formName 为空时提交 |
| 活动类型为空 | `请选择活动类型` | #formType 未选中时提交 |
| 子类型为空 | `请选择子类型` | community/family 但未选子类型时提交 |
| 开始时间为空 | `请选择开始时间` | #formStartTime 为空时提交 |
| 结束时间为空 | `请选择结束时间` | #formEndTime 为空时提交 |
| 时间范围无效 | `结束时间必须晚于开始时间` | 结束 ≤ 开始 |
| 时长超限 | `活动时长不能超过72小时` | 时长 > 72 小时 |
| 活动简介为空 | `请输入活动简介` | #formDescription 为空时提交 |

### 8.2 预期的成功消息

从 `config/activity.yaml` → `success_messages:` 获取：

| 场景 | 预期 toast 文本 |
|------|---------------|
| 创建成功 | `活动创建成功` |
| 保存草稿（完整） | `草稿已保存，稍后可以继续编辑` |
| 保存草稿（仅名称） | `草稿已保存` |
| 取消成功 | `已取消` |
| 删除成功 | `已删除` |

### 8.3 断言写法

```python
# 正确：使用 conftest helper + assert
toast_text = get_toast_text(page)
assert "活动创建成功" in toast_text, \
    f"期望 toast 包含'活动创建成功'，实际: {toast_text}"

error_text = get_error_text(page, "formName")
assert "请输入活动名称" in error_text, \
    f"期望错误'请输入活动名称'，实际: {error_text}"

# 正确：Playwright expect 用于元素状态
expect(page.locator("#subTypeDiv")).to_be_visible()
expect(page.locator("#formOtherType")).to_be_visible()

# 正确：input_value 获取表单值
assert page.input_value("#formName") == "测试活动", "活动名称应保留"

# 错误：不要在 helper 函数中写 assert
# 错误：不要使用硬编码文本进行完整匹配
#     toast_text == "活动创建成功"  # 太脆弱，toast 可能含额外文本
```

### 8.4 验证顺序注意事项

根据 `validateForm()` 逻辑，错误消息按以下顺序返回（一次只显示一个）：

1. 活动名称为空 → `请输入活动名称`
2. 活动类型为空 → `请选择活动类型`
3. 子类型为空 → `请选择子类型`（仅 community/family）
4. 开始时间为空 → `请选择开始时间`
5. 结束时间为空 → `请选择结束时间`
6. 结束时间 ≤ 开始时间 → `结束时间必须晚于开始时间`
7. 时长 > 72h → `活动时长不能超过72小时`
8. 活动简介为空 → `请输入活动简介`

因此，当仅需验证特定字段错误时，必须先确保该字段之前的所有必填字段都已正确填写，否则会得到更早的错误提示。

---

## 快速启动清单

生成测试文件的典型工作流：

1. **打开 `config/activity.yaml`** → 掌握选择器映射和错误消息
2. **打开目标 `Requirements/活动管理_{NN}_{模块}.md`** → 提取 TC 编号和测试场景
3. **打开 `test/ai/generated/activity/conftest.py`** → 了解可用的 helper 和 fixtures
4. **生成测试文件** → 按上述模板生成，输出到 `test/ai/generated/activity/test_{module}.py`
5. **运行验证** → `pytest test/ai/generated/activity/test_{module}.py -v --browser=chromium`
