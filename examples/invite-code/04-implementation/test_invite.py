"""Invite-code join — TESTS (pipeline step 4: written by the reviewer from the
approved behavior checklist, before any implementation exists).

Every test maps 1:1 to a behavior case ID in ../02-behavior-cases.md.
Run:  python3 -m unittest test_invite -v
"""

import unittest

from invite import InviteError, InviteService


class FakeClock:
    def __init__(self, now=1_700_000_000):
        self.now = now

    def __call__(self):
        return self.now


def fresh_service():
    clock = FakeClock()
    svc = InviteService(clock=clock)
    # Workspace W1, code valid for 7 days, 5 uses.
    svc.create_code(workspace_id="W1", code="JOIN42", ttl_seconds=7 * 24 * 3600, max_uses=5)
    return svc, clock


class TestInviteJoin(unittest.TestCase):
    def test_INV_001_valid_code_joins_workspace(self):
        svc, _ = fresh_service()
        result = svc.join(user_id="u1", raw_code="JOIN42")
        self.assertEqual(result.workspace_id, "W1")
        self.assertTrue(svc.is_member("W1", "u1"))

    def test_INV_002_expired_code_is_rejected(self):
        svc, clock = fresh_service()
        clock.now += 8 * 24 * 3600  # past the 7-day expiry
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="u1", raw_code="JOIN42")
        self.assertEqual(ctx.exception.code, "INVITE_EXPIRED")
        self.assertFalse(svc.is_member("W1", "u1"))

    def test_INV_003_exhausted_code_is_rejected(self):
        svc, _ = fresh_service()
        for i in range(5):
            svc.join(user_id=f"u{i}", raw_code="JOIN42")
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="u6", raw_code="JOIN42")
        self.assertEqual(ctx.exception.code, "INVITE_EXHAUSTED")
        self.assertFalse(svc.is_member("W1", "u6"))

    def test_INV_004_unknown_code_generic_error_no_workspace_leak(self):
        svc, _ = fresh_service()
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="u1", raw_code="NOPE99")
        self.assertEqual(ctx.exception.code, "INVITE_NOT_FOUND")
        # The error must not reveal whether any workspace uses a similar code.
        self.assertNotIn("W1", ctx.exception.message)

    def test_INV_005_existing_member_cannot_join_twice(self):
        svc, _ = fresh_service()
        svc.join(user_id="u1", raw_code="JOIN42")
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="u1", raw_code="JOIN42")
        self.assertEqual(ctx.exception.code, "ALREADY_MEMBER")

    def test_INV_006_repeated_guessing_is_rate_limited(self):
        svc, _ = fresh_service()
        for _ in range(10):
            with self.assertRaises(InviteError):
                svc.join(user_id="attacker", raw_code="GUESS1")
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="attacker", raw_code="JOIN42")  # even the right code
        self.assertEqual(ctx.exception.code, "RATE_LIMITED")

    def test_INV_007_regenerated_code_invalidates_the_old_one(self):
        svc, _ = fresh_service()
        svc.create_code(workspace_id="W1", code="NEW777", ttl_seconds=3600, max_uses=5)
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="u1", raw_code="JOIN42")
        self.assertEqual(ctx.exception.code, "INVITE_NOT_FOUND")
        result = svc.join(user_id="u1", raw_code="NEW777")
        self.assertEqual(result.workspace_id, "W1")

    def test_INV_008_code_input_is_normalized(self):
        svc, _ = fresh_service()
        result = svc.join(user_id="u1", raw_code="  join42 ")
        self.assertEqual(result.workspace_id, "W1")

    # --- Hidden scenarios: kept by the reviewer, run only in the final round,
    # --- unsealed into the case file after merge (see ../06-archive-state.md).

    def test_INV_H1_failed_attempts_count_even_for_malformed_codes(self):
        svc, _ = fresh_service()
        for bad in ["", "x", "!!", "toolongcode123", "JOIN4", "JOIN43", "JOIN44", "JOIN45", "JOIN46", "JOIN47"]:
            with self.assertRaises(InviteError):
                svc.join(user_id="prober", raw_code=bad)
        with self.assertRaises(InviteError) as ctx:
            svc.join(user_id="prober", raw_code="JOIN42")
        self.assertEqual(ctx.exception.code, "RATE_LIMITED")

    def test_INV_H2_rate_limit_is_per_user_not_global(self):
        svc, _ = fresh_service()
        for _ in range(10):
            with self.assertRaises(InviteError):
                svc.join(user_id="attacker", raw_code="GUESS1")
        # Another user is unaffected by the attacker's limit.
        result = svc.join(user_id="innocent", raw_code="JOIN42")
        self.assertEqual(result.workspace_id, "W1")


if __name__ == "__main__":
    unittest.main()
