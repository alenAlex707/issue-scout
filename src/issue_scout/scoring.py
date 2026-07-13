from __future__ import annotations

from datetime import datetime, timezone

from issue_scout.models import IssueCandidate, ScoreBreakdown


def score_issue(issue: IssueCandidate, *, now: datetime | None = None) -> ScoreBreakdown:
    """Score an issue using transparent, deterministic heuristics."""
    now = now or datetime.now(timezone.utc)
    labels = {label.casefold() for label in issue.labels}
    score = 0
    reasons: list[str] = []

    for label, points, reason in [
        ("good first issue", 30, "good first issue label"),
        ("help wanted", 20, "help wanted label"),
        ("bug", 8, "bug label"),
        ("documentation", 6, "documentation label"),
    ]:
        if label in labels:
            score += points
            reasons.append(f"+{points} {reason}")

    if not issue.assignees:
        score += 15
        reasons.append("+15 unassigned")
    else:
        score -= 25
        reasons.append("-25 already assigned")

    age_days = max(0, (now - issue.updated_at).days)
    freshness = 15 if age_days <= 7 else 10 if age_days <= 30 else 5 if age_days <= 90 else 0
    if freshness:
        score += freshness
        reasons.append(f"+{freshness} updated {age_days}d ago")

    body_length = len(issue.body.strip())
    if body_length >= 200:
        score += 8
        reasons.append("+8 detailed description")
    elif body_length >= 50:
        score += 4
        reasons.append("+4 useful description")

    comment_penalty = min(15, issue.comments * 2)
    if comment_penalty:
        score -= comment_penalty
        reasons.append(f"-{comment_penalty} discussion activity")

    if issue.linked_open_pull_request:
        score -= 50
        reasons.append("-50 linked open pull request")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
