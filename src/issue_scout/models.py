from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class IssueCandidate:
    """Normalized subset of a GitHub issue search result."""

    repository: str
    number: int
    title: str
    url: str
    body: str
    labels: tuple[str, ...]
    assignees: tuple[str, ...]
    comments: int
    created_at: datetime
    updated_at: datetime
    linked_open_pull_request: bool = False

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> IssueCandidate:
        repository_url = payload.get("repository_url", "")
        repository = repository_url.rsplit("/repos/", 1)[-1]
        return cls(
            repository=repository,
            number=int(payload["number"]),
            title=str(payload["title"]),
            url=str(payload["html_url"]),
            body=str(payload.get("body") or ""),
            labels=tuple(str(label["name"]) for label in payload.get("labels", [])),
            assignees=tuple(str(user["login"]) for user in payload.get("assignees", [])),
            comments=int(payload.get("comments", 0)),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
        )

    def with_linked_pr(self, linked: bool) -> IssueCandidate:
        values = self.__dict__ | {"linked_open_pull_request": linked}
        return type(self)(**values)


@dataclass(frozen=True)
class ScoreBreakdown:
    """A candidate's final score and human-readable reasons."""

    score: int
    reasons: tuple[str, ...]


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
