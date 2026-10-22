[English](02-red-evidence.md) | 简体中文

# 紧急修复证据——回归测试先跑红、再跑绿（Issue #137）

## 回归用例从哪来

这个行为不是新的，它的用例也不是。归档的本功能清单（[02](../invite-code/02-behavior-cases.zh-CN.md)）里已经有：

- **INV-002 Expired code rejected**（过期码被拒绝）——Given 一个已过期的码，When 一个非成员提交它，Then 加入以"已过期"被拒绝，且不创建成员关系。

——而契约（[01](../invite-code/01-issue-intent.zh-CN.md) §Interface）也已经写明了要求的错误码：`INVITE_EXPIRED`（410）。一直没有被钉住的是*错误信封*：INV-002 在第 4 步的测试断言的是服务的域结果，而域结果一直是对的。回归测试 **HF-001** 是把 INV-002 在响应错误信封层重新断言一次——正是 bug 真正所在的那一层。同一个映射表相邻的三行，在同一个文件里一并加上错误信封钉测，这样修复就不会把穿落悄悄挪到别处。

测试和功能的代码放在一起，在 `examples/invite-code/04-implementation/test_invite_hotfix.py`（stdlib `unittest`，与功能测试套件相同）。

## 跑红（修复前）

```text
$ python3 -m unittest test_invite_hotfix -v
test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping) ... FAIL
test_pin_exhausted_reports_exhausted (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_revoked_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_unknown_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok

======================================================================
FAIL: test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_invite_hotfix.py", line 38, in test_hf_001_expired_reports_expired
    self.assertEqual(resp.error_code, "INVITE_EXPIRED")
AssertionError: 'INVITE_NOT_FOUND' != 'INVITE_EXPIRED'
- INVITE_NOT_FOUND
+ INVITE_EXPIRED

----------------------------------------------------------------------
Ran 4 tests in 0.003s

FAILED (failures=1)
```

只有一个失败——正是报上来的那个 bug，已复现。三个相邻钉测都通过，确认穿落只影响缺失的那一行。

## 修复

错误映射层加上一行：`EXPIRED` 服务结果现在映射到 `INVITE_EXPIRED`（410），并带上它面向用户的文案。没有动任何业务逻辑。

## 跑绿（修复后）

```text
$ python3 -m unittest test_invite_hotfix -v
test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_exhausted_reports_exhausted (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_revoked_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_unknown_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK
```

完整套件（功能 + 紧急修复）：14 个测试，OK——已记录在对账单（03）中。
