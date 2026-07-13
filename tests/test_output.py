import csv
import io
import json

from issue_scout.output import RankedIssue, render
from issue_scout.scoring import score_issue


def ranked(candidate_factory):
    issue = candidate_factory()
    return RankedIssue(issue=issue, ranking=score_issue(issue))


def test_json_output(candidate_factory):
    stream = io.StringIO()
    render([ranked(candidate_factory)], "json", stream=stream)
    payload = json.loads(stream.getvalue())
    assert payload[0]["repository"] == "octo/demo"
    assert payload[0]["number"] == 42


def test_csv_output(candidate_factory):
    stream = io.StringIO()
    render([ranked(candidate_factory)], "csv", stream=stream)
    row = next(csv.DictReader(io.StringIO(stream.getvalue())))
    assert row["repository"] == "octo/demo"
    assert row["linked_open_pr"] == "False"


def test_empty_table():
    stream = io.StringIO()
    render([], "table", stream=stream)
    assert stream.getvalue() == "No matching issues found.\n"


def test_table_contains_reference_and_url(candidate_factory):
    stream = io.StringIO()
    render([ranked(candidate_factory)], "table", stream=stream)
    assert "octo/demo#42" in stream.getvalue()
    assert "https://github.com/octo/demo/issues/42" in stream.getvalue()
