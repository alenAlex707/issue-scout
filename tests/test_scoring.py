from datetime import datetime, timezone

from issue_scout.scoring import score_issue

NOW = datetime(2026, 7, 13, tzinfo=timezone.utc)


def test_strong_candidate_score(candidate_factory):
    ranking = score_issue(candidate_factory(), now=NOW)

    assert ranking.score == 86
    assert "+30 good first issue label" in ranking.reasons
    assert "+15 unassigned" in ranking.reasons


def test_assignment_and_discussion_penalties(candidate_factory):
    ranking = score_issue(candidate_factory(assignees=("maintainer",), comments=20), now=NOW)

    assert ranking.score == 33
    assert "-25 already assigned" in ranking.reasons
    assert "-15 discussion activity" in ranking.reasons


def test_linked_pull_request_penalty(candidate_factory):
    regular = score_issue(candidate_factory(), now=NOW)
    linked = score_issue(candidate_factory(linked_open_pull_request=True), now=NOW)

    assert linked.score == regular.score - 50


def test_old_issue_gets_no_freshness_bonus(candidate_factory):
    issue = candidate_factory(updated_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    ranking = score_issue(issue, now=NOW)

    assert not any("updated" in reason for reason in ranking.reasons)
