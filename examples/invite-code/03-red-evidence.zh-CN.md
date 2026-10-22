[English](03-red-evidence.md) | 简体中文

# 第 4 步产物 — 独立测试与跑红证据

Reviewer 只依据已批准的行为清单（02）写出了 `04-implementation/test_invite.py`——8 个测试，一条用例一个，按用例 ID 命名。另外还有两条额外场景被 Reviewer 保留为**隐藏**（INV-H1、INV-H2）；它们存在于测试文件的隐藏区，但没有向 Writer 披露，也不计入第 3 步的批准范围。

## 跑红（实现之前，测试对桩运行）

Writer 提供了一个桩服务，其方法一律抛出 `NotImplementedError`（`invite_stub.py.txt`）。拿 Reviewer 的测试对它跑：

```text
$ python3 -m unittest test_invite
Ran 10 tests in 0.002s

FAILED (errors=10)
```

（10 = 8 条已披露 + 2 条隐藏，全部失败，因为行为尚不存在。如果某个测试在这里*通过*了，那它就是无效的——它什么都没证明。）

## 冻结记录

- 测试就此冻结。第 5 步期间 Writer 不得修改它们；任何改动都要回到第 3 步验收门重新批准。
- 行为清单也已用人话发到 issue #101（「每个测试在测什么……」），决策者已确认。第 5 步可以开始。
