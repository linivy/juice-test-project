---
name: issue-format
description: GitHub Issue 格式规范（用于自动创建的 Bug 报告）
trigger: manual
type: documentation
---

## Issue 标题格式

- **格式**: `【优先级】【模块】问题描述 - 运行 #编号`
- **示例**: `🟡【UI测试失败】test_product_card_fields - 运行 #50`

### 优先级标签

| 优先级 | 图标 | 条件 | 标签 |
|--------|------|------|------|
| Critical | 🔴 | 5+ 测试失败 | `priority-critical` |
| High | 🟠 | 3-4 测试失败 | `priority-high` |
| Medium | 🟡 | 1-2 测试失败 | `priority-medium` |
| Low | 🟢 | 1 个测试失败 | `priority-low` |

## Issue 内容模板

```markdown
## 🐛 Bug 描述

测试执行失败，🟡 **medium** 优先级

---

## 📊 测试概览

| 指标 | 详情 |
|------|------|
| 📋 运行编号 | [#50](链接) |
| 🔀 触发方式 | push |
| 🌿 分支 | main |
| 📝 提交 | [abc1234](链接) |
| 👤 触发用户 | @username |
| 📈 失败率 | 5.00% |

### 测试统计

| 类型 | 数量 |
|------|------|
| ✅ 通过 | 19 |
| ❌ 失败 | 1 |
| 📊 总计 | 20 |

---

## ❌ 失败的测试用例

---

test/list/test_product_list.py::test_product_card_fields[chromium] FAILED

---

## 📝 错误详情

AssertionError: 断言失败信息...

---

## 📸 自动捕获的资源

| 资源类型 | 说明 |
|----------|------|
| 🖼️ 页面截图 | 失败时的完整页面截图 |
| 🎬 测试视频 | 测试过程录屏 |
| 📄 页面源码 | 失败时的 HTML 源码 |
| 📝 控制台日志 | 浏览器控制台输出 |

**📥 下载地址**: [Actions Artifacts](链接)

---

## 🔄 复现步骤

```bash
# 1. 克隆仓库
git clone https://github.com/repo.git
cd repo

# 2. 切换到失败提交
git checkout abc1234

# 3. 安装依赖
pip install pytest pytest-playwright
playwright install chromium

# 4. 启动 Juice Shop
docker run -d -p 3000:3000 bkimminich/juice-shop
sleep 10

# 5. 运行失败的测试
pytest test/list/ -v
```

---

## 🔗 相关链接

- 📊 [查看详细运行日志](链接)
- 📁 [查看失败测试代码](链接)
- 🌐 [Juice Shop 应用](http://localhost:3000)

---

## 🔧 处理建议

1. **查看日志**: 点击上方链接查看详细失败日志
2. **分析截图**: 下载 Artifact 中的截图分析页面状态
3. **本地复现**: 使用上方"复现步骤"在本地复现问题
4. **定位修复**: 根据错误信息定位并修复代码
5. **提交 PR**: 使用 `fixes #N` 格式提交修复 PR

---

> 🤖 *此 Issue 由 GitHub Actions 自动创建*
> 🧪 测试框架: pytest + Playwright
> 📱 类型: UI 自动化测试
> ⏰ 创建时间: 2026-04-28 10:30:00
```

## Issue 标签规范

| 标签 | 说明 |
|------|------|
| `bug` | 表示这是一个 Bug |
| `auto-reported` | 表示这是自动创建的 Issue |
| `testing` | 表示与测试相关 |
| `priority-critical` | 严重优先级 |
| `priority-high` | 高优先级 |
| `priority-medium` | 中等优先级 |
| `priority-low` | 低优先级 |

## 自动创建逻辑

1. **触发条件**: 只有当测试失败且事件类型为 `push` 时才创建 Issue
2. **优先级计算**: 根据失败测试数量自动确定优先级
3. **标签添加**: 自动添加 `bug`, `auto-reported`, `testing` 和对应的优先级标签
4. **重复检测**: 如果相同的失败 Issue 已存在，跳过创建
5. **Artifact 上传**: 自动上传截图、视频、日志等资源