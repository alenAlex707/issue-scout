from datetime import datetime, timezone

import pytest

from issue_scout.models import IssueCandidate


@pytest.fixture
def candidate_factory():
    def factory(**overrides):
        values = {
            "repository": "octo/demo",
            "number": 42,
            "title": "Improve error handling",
            "url": "https://github.com/octo/demo/issues/42",
            "body": "A clear description of the problem and the expected behavior. " * 4,
            "labels": ("good first issue", "help wanted"),
            "assignees": (),
            "comments": 1,
            "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "updated_at": datetime(2026, 7, 10, tzinfo=timezone.utc),
            "linked_open_pull_request": False,
        }
        values.update(overrides)
        return IssueCandidate(**values)

    return factory
