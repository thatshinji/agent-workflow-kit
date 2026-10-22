"""Invite-code join — implementation (pipeline step 5: minimal GREEN).

In-memory stores keep the example self-contained; a production version puts
the same rules behind the repository layer and the contract's error envelope.
Behavior follows ../02-behavior-cases.md case by case (IDs in comments).
"""

from dataclasses import dataclass, field

MAX_FAILED_ATTEMPTS = 10       # per user, per window (INV-006)
ATTEMPT_WINDOW_SECONDS = 3600  # 1 hour


class InviteError(Exception):
    """Business error carrying the contract's error code + a plain message."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass
class InviteCode:
    code: str
    workspace_id: str
    expires_at: float
    max_uses: int
    uses: int = 0
    revoked: bool = False


@dataclass
class JoinResult:
    workspace_id: str
    user_id: str


@dataclass
class InviteService:
    clock: object  # callable returning epoch seconds
    _codes: dict = field(default_factory=dict)        # normalized code -> InviteCode
    _members: dict = field(default_factory=dict)      # workspace_id -> set(user_id)
    _attempts: dict = field(default_factory=dict)     # user_id -> list[timestamps]

    # -- admin side ---------------------------------------------------------
    def create_code(self, workspace_id, code, ttl_seconds, max_uses):
        normalized = self._normalize(code)
        # A workspace has exactly one live code: issuing a new one revokes
        # the previous (INV-007).
        for existing in self._codes.values():
            if existing.workspace_id == workspace_id and not existing.revoked:
                existing.revoked = True
        invite = InviteCode(
            code=normalized,
            workspace_id=workspace_id,
            expires_at=self.clock() + ttl_seconds,
            max_uses=max_uses,
        )
        self._codes[normalized] = invite
        return invite

    # -- member side --------------------------------------------------------
    def join(self, user_id, raw_code):
        self._check_rate_limit(user_id)  # INV-006 / INV-H1 / INV-H2
        normalized = self._normalize(raw_code)
        invite = self._codes.get(normalized)
        if invite is None or invite.revoked:
            self._record_failure(user_id)
            # Generic on purpose: never leak which workspace a code
            # belongs to, or whether a similar code exists (INV-004).
            raise InviteError("INVITE_NOT_FOUND", "That invite code isn't valid.")
        if self.clock() > invite.expires_at:
            self._record_failure(user_id)
            raise InviteError("INVITE_EXPIRED", "That invite code has expired.")
        if invite.uses >= invite.max_uses:
            self._record_failure(user_id)
            raise InviteError("INVITE_EXHAUSTED", "That invite code has no uses left.")
        if self.is_member(invite.workspace_id, user_id):
            raise InviteError("ALREADY_MEMBER", "You're already a member of this workspace.")
        invite.uses += 1
        self._members.setdefault(invite.workspace_id, set()).add(user_id)
        return JoinResult(workspace_id=invite.workspace_id, user_id=user_id)

    def is_member(self, workspace_id, user_id):
        return user_id in self._members.get(workspace_id, set())

    # -- internals ----------------------------------------------------------
    @staticmethod
    def _normalize(raw_code):
        return raw_code.strip().upper()  # INV-008

    def _recent_failures(self, user_id):
        now = self.clock()
        attempts = [t for t in self._attempts.get(user_id, []) if now - t < ATTEMPT_WINDOW_SECONDS]
        self._attempts[user_id] = attempts
        return attempts

    def _check_rate_limit(self, user_id):
        if len(self._recent_failures(user_id)) >= MAX_FAILED_ATTEMPTS:
            raise InviteError("RATE_LIMITED", "Too many attempts. Try again later.")

    def _record_failure(self, user_id):
        self._recent_failures(user_id).append(self.clock())
