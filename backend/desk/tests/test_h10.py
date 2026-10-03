from django.test import TestCase

from desk.auth_utils import create_access_token, hash_password
from desk.models import OffsetSubmission, User


def _make_user(username: str, role: str) -> User:
    return User.objects.create(
        username=username,
        role=role,
        password=hash_password("x" * 10),
        is_active=True,
    )


def _auth(user: User) -> dict:
    return {"HTTP_AUTHORIZATION": f"Bearer {create_access_token(user)}"}


class OverviewListTests(TestCase):
    """H10: once a submission lands, the overview must show it immediately —

    no row may stay hidden under the old "organizing" filter.
    """

    def setUp(self):
        self.machinist = _make_user("machinist", User.Role.MACHINIST)
        self.auditor = _make_user("auditor", User.Role.AUDITOR)

    def _create(self, tool_code: str, offset_um: int) -> int:
        resp = self.client.post(
            "/api/submissions",
            data={"tool_code": tool_code, "offset_um": offset_um},
            content_type="application/json",
            **_auth(self.machinist),
        )
        assert resp.status_code == 200, resp.content
        return resp.json()["id"]

    def _list_ids(self, user=None) -> list[int]:
        resp = self.client.get("/api/submissions", **_auth(user or self.machinist))
        assert resp.status_code == 200, resp.content
        return [row["id"] for row in resp.json()]

    def test_newest_submission_visible_immediately(self):
        new_id = self._create("T01", 5)
        assert new_id in self._list_ids()

    def test_pass_and_fail_both_visible_after_refresh(self):
        pass_id = self._create("T02", 5)    # |5| <= 12 → 合格
        fail_id = self._create("T03", 20)   # |20| > 12 → 超差
        ids = self._list_ids()
        assert pass_id in ids
        assert fail_id in ids

    def test_rapid_successive_submissions_all_visible(self):
        ids = [self._create(f"T1{i}", i) for i in range(5)]
        listed = self._list_ids()
        for new_id in ids:
            assert new_id in listed

    def test_newest_visible_to_auditor_too(self):
        new_id = self._create("T20", 3)
        assert new_id in self._list_ids(user=self.auditor)

    def test_detail_still_openable(self):
        new_id = self._create("T21", 7)
        resp = self.client.get(f"/api/submissions/{new_id}", **_auth(self.machinist))
        assert resp.status_code == 200
        assert resp.json()["id"] == new_id


class ReadOnlyAuditorTests(TestCase):
    """复核员身份保持只读，不能提交刀补。"""

    def setUp(self):
        self.auditor = _make_user("auditor", User.Role.AUDITOR)

    def test_auditor_cannot_submit(self):
        resp = self.client.post(
            "/api/submissions",
            data={"tool_code": "T99", "offset_um": 1},
            content_type="application/json",
            **_auth(self.auditor),
        )
        assert resp.status_code == 403
        assert OffsetSubmission.objects.count() == 0

    def test_auditor_has_no_write_flag(self):
        assert self.auditor.can_write is False
