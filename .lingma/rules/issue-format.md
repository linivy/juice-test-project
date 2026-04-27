---
name: issue-format
description: GitHub Issue 格式规范（用于自动创建的 Bug 报告）
trigger: manual
type: documentation
---

## Issue 标题格式

- 格式：`【模块】问题描述 - 运行 #编号`
- 示例：`【UI测试失败】test_refund_with_invalid_order_id - 运行 #50`

## Issue 内容模板

```markdown
## 🐛 Bug 描述

**问题摘要**: [简短描述问题]

---

### 实际结果 (Actual Result)

- [具体描述实际发生的情况]

---

### 期望结果 (Expected Result)

- [具体描述应该发生的情况]

---

### 失败的测试详情

| 测试用例 | 错误信息 |
| --- | --- |
| test_xxx.py::test_xxx | TimeoutError: ... |

---

### 📎 相关信息

| 项目 | 信息 |
| --- | --- |
| 运行编号 | #123 |
| 运行时间 | 2026-04-10 08:00:00 |
| 触发方式 | 定时任务 / UI 测试 / push |
| 触发用户 | @username |

---

### 🔗 相关链接

- [查看详细运行日志](链接)
- [查看提交详情](链接)

---

### 📸 截图附件

截图已上传为 Artifact，请在 Actions 运行页面下载 `screenshots` 查看。

---

### 🔧 处理建议

1. 点击上方"查看详细运行日志"链接，确认失败原因
2. 根据"实际结果"和"期望结果"的差异，定位代码问题
3. 修复后，使用 `fixes #Issue编号` 提交代码
4. 此 Issue 会在 PR 合并后自动关闭

---
*此 Issue 由 GitHub Actions 自动创建 | 测试类型: UI 自动化*