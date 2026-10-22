English | [简体中文](03-red-evidence.zh-CN.md)

# Step 4 artifact — Independent tests & red evidence

The reviewer wrote `04-implementation/test_invite.py` from the approved checklist (02) alone — 8 tests, one per case, named by case ID. Two additional scenarios were kept **hidden** by the reviewer (INV-H1, INV-H2); they exist in the test file's hidden section but were not disclosed to the writer and are not counted in the step-3 approval.

## Red run (tests vs. the stub, before implementation)

The writer provided a stub service whose methods raise `NotImplementedError` (`invite_stub.py.txt`). Running the reviewer's tests against it:

```text
$ python3 -m unittest test_invite
Ran 10 tests in 0.002s

FAILED (errors=10)
```

(10 = 8 disclosed + 2 hidden, all failing because the behavior does not exist yet. A test that *passed* here would be invalid — it would prove nothing.)

## Freeze record

- Tests frozen at this state. The writer may not modify them during step 5; any change returns to the step-3 gate for re-approval.
- The checklist was also posted to issue #101 in plain language ("each test checks that…"), and the decision-maker confirmed it. Step 5 may begin.
