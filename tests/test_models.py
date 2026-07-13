from datetime import datetime, timezone

from issue_scout.models import IssueCandidate


def test_candidate_from_api():
    issue = IssueCandidate.from_api(
        {
            "repository_url": "https://api.github.com/repos/octo/demo",
            "number": 7,
            "title": "Document the API",
            "html_url": "https://github.com/octo/demo/issues/7",
            "body": None,
            "labels": [{"name": "documentation"}],
            "assignees": [{"login": "octocat"}],
            "comments": 3,
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-02-01T12:30:00Z",
        }
    )

    assert issue.repository == "octo/demo"
    assert issue.labels == ("documentation",)
    assert issue.assignees == ("octocat",)
    assert issue.body == ""
    assert issue.updated_at == datetime(2026, 2, 1, 12, 30, tzinfo=timezone.utc)


def test_with_linked_pr_is_immutable(candidate_factory):
    original = candidate_factory()
    updated = original.with_linked_pr(True)

    assert original.linked_open_pull_request is False
    assert updated.linked_open_pull_request is True
    assert updated.number == original.number
