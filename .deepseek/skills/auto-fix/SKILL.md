---
name: auto-fix
description: Use when pytest tests fail and the user provides error logs, or when the user asks to "fix failing tests", "debug tests", or "auto-fix" test failures. Analyzes pytest output to diagnose and repair Playwright+pytest test code.
---

# Auto-Fix for Pytest + Playwright Tests

Diagnose failing pytest tests from error logs, apply targeted fixes, and prompt
re-run verification. Works standalone or paired with `activity-test`.

---

## 1. Failure Classifier

Parse pytest output and classify each failure into one of the following types.
A single failure may match multiple types — address them in order of severity
(P0 first).

### P0 — Selector / Locator Failures

**Symptom patterns in logs:**

```
TimeoutError: Timeout 5000ms exceeded.
waiting for selector "#wrongId"
Error: locator.fill: target not found
Error: locator.click: element is not visible
```

**Root causes:**
- Selector string does not match any DOM element (typo, renamed ID)
- Element exists but is hidden (wrong cascade state, style display none)
- Wrong selector format (e.g. fill on a contenteditable div)

**Fix actions:**
1. Cross-reference the failing selector against `config/activity.yaml` `selectors`
2. If selector is in yaml: replace hard-coded string with `page.fill(SEL["name"], value)`
3. If selector not in yaml: read `demo/activity_management.html` to find the actual id
4. Apply the fix directly via `edit_file`

### P1 — Timing / Wait Failures

**Symptom patterns:**

```
TimeoutError: waiting for selector "#subTypeDiv" to be visible
playwright._impl._errors.TimeoutError
```

**Root causes:**
- Element needs a prior interaction before appearing (cascade trigger not fired)
- `wait_for_timeout` too short for API response
- Selector visibility condition is wrong (element is in DOM but display none)

**Fix actions:**
1. Identify the missing prerequisite step (e.g. selecting formType before subTypeDiv)
2. Add the missing `page.select_option(...)` or `page.click(...)` before the wait
3. If the element uses style.display toggling (not `.show` class), use:
   ```python
   page.wait_for_selector("#subTypeDiv:not([style*='display: none'])", timeout=3000)
   ```
4. Increase timeout from static value to `TMO.get("cascade_api", 500)` if cascade-related

### P2 — Assertion Failures

**Symptom patterns:**

```
AssertionError: assert "活动创建成功" in "活动信息未完善，请前往完善"
E   assert False
```

**Root causes:**
- Wrong expected string (error message from wrong validation stage)
- Validation order: earlier field failed, cascading to a different error than expected
- Toast created before modal confirmed, or vice versa

**Fix actions:**
1. Check validateForm() order in demo/activity_management.html — errors return one at a time
2. If testing a specific field error, ensure all earlier required fields are filled
3. Update the expected error string to match the actual value from the log
4. If toast assertion fails: verify whether a confirm modal step is missing

### P3 — Modal / Dialog Failures

**Symptom patterns:**

```
Error: locator.click: element intercepts pointer
Error: locator.click: target is not clickable
```

**Root causes:**
- Expected modal did not appear (validation passed without modal)
- Wrong button selector inside modal
- Modal `.show` class not present

**Fix actions:**
1. Check actual modal button IDs in `demo/activity_management.html`:
   - confirmModal: btnConfirm (ok), btnConfirmCancelBtn (cancel)
   - cancelModal: btnConfirmCancel (ok), btnCloseCancelModal (close)
2. Ensure `page.wait_for_selector("#confirmModal.show")` before clicking modal buttons
3. Add `page.wait_for_timeout(300)` after modal clicks for animation

### P4 — Environment / Import Failures

**Symptom patterns:**

```
ModuleNotFoundError: No module named 'yaml'
ImportError: cannot import name 'SEL'
```

**Root causes:**
- Missing `pip install pyyaml` after conftest refactoring
- Wrong import path in test file

**Fix actions:**
1. If `No module named 'yaml'`: instruct user to run `pip install pyyaml`
2. If import error: verify `from test.ai.generated.activity.conftest import ...` path
3. Do NOT modify test file imports unless they are genuinely wrong

---

## 2. Fix Workflow

```
pytest error log → classify failure type → read relevant source → apply edit → prompt re-run
```

### Step-by-step

1. **Parse the log** — Extract every FAILED line with its traceback
2. **Classify** — Tag each failure with the type(s) from Section 1
3. **Read source** — Open the test file at the failing line number from the traceback
4. **Read config** — If selector-related, open `config/activity.yaml`
5. **Read HTML** — If selector not found in yaml, grep `demo/activity_management.html`
6. **Apply fix** — Use `edit_file` with precise search/replace
7. **Report** — Output a table: failure → root cause → fix applied → re-run command

### Re-run prompt format after fixes

```
Fixes applied. Re-run:

  pytest {failing_test_path} -v --tb=short

Summary:
  {file}: {change_description}
```

---

## 3. Common Fix Patterns

### Pattern A: Selector typo
```python
# Before (failing)
page.fill("#formname", "test")

# After (fixed)
page.fill(SEL["form_name"], "test")
```

### Pattern B: Missing cascade prerequisite
```python
# Before (failing — TimeoutError waiting for #subTypeDiv)
page.wait_for_selector("#subTypeDiv:not([style*='display: none'])")

# After (fixed)
page.select_option(SEL["form_type"], "community")
page.wait_for_selector("#subTypeDiv:not([style*='display: none'])")
```

### Pattern C: Wrong modal button
```python
# Before (failing — button not found in confirm modal)
page.click("#confirmModal #btnCancel")

# After (fixed)
page.click(SEL["btn_confirm_cancel_btn"])
```

### Pattern D: Validation order mismatch
```python
# Before — expected "请选择活动类型" but got earlier error "请输入活动名称"
page.select_option(SEL["form_type"], "community")
submit_create(page)
assert "请选择活动类型" in get_error_text(page, "formType")

# After — fill name first since it validates earlier
page.fill(SEL["form_name"], "测试活动")
page.select_option(SEL["form_type"], "community")
submit_create(page)
assert "请选择活动类型" in get_error_text(page, "formType")
```

### Pattern E: Flatpickr date setting
```python
# Before — page.fill does nothing on flatpickr input
page.fill("#formStartTime", "2026-06-20 09:00")

# After — use evaluate + flatpickr API
page.locator("#formStartTime").click()
page.evaluate(
    """([sel, date]) => {
        const el = document.querySelector(sel);
        if (el && el._flatpickr) el._flatpickr.setDate(date);
    }""",
    ["#formStartTime", "2026-06-20 09:00"],
)
page.keyboard.press("Escape")
```

### Pattern F: contenteditable fill
```python
# Before — page.fill on contenteditable div has no effect
page.fill("#formDescription", "简介")

# After — set innerHTML + dispatch input event
page.evaluate(
    """([sel, html]) => {
        const el = document.querySelector(sel);
        if (el) {
            el.innerHTML = html;
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }""",
    ["#formDescription", "<p>简介</p>"],
)
```

---

## 4. Constraints

- Do NOT change function signatures in conftest.py during auto-fix
- Do NOT change test method names or TC IDs
- Preserve Chinese comments and docstrings
- If a failure has no clear fix, flag it for manual review rather than guessing
- If the fix requires a yaml change, apply it to `config/activity.yaml` as well
- Always verify the fix does not break other tests by checking for cross-references
