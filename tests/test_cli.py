import issue_scout.cli


class FakeClient:
    issues = []

    def __init__(self, token=None):
        self.token = token

    def search_issues(self, query, *, limit):
        assert 'language:"Python"' in query
        assert limit == 5
        return self.issues

    def has_linked_open_pull_request(self, issue):
        return issue.linked_open_pull_request


def test_cli_json(monkeypatch, capsys, candidate_factory):
    FakeClient.issues = [candidate_factory()]
    monkeypatch.setattr(issue_scout.cli, "GitHubClient", FakeClient)

    result = issue_scout.cli.run(["--limit", "5", "--format", "json"])

    assert result == 0
    assert '"repository": "octo/demo"' in capsys.readouterr().out


def test_cli_filters_linked_pr(monkeypatch, capsys, candidate_factory):
    FakeClient.issues = [candidate_factory(linked_open_pull_request=True)]
    monkeypatch.setattr(issue_scout.cli, "GitHubClient", FakeClient)

    assert issue_scout.cli.run(["--limit", "5"]) == 0
    assert capsys.readouterr().out == "No matching issues found.\n"


def test_cli_reports_invalid_repository(capsys):
    assert issue_scout.cli.run(["--repo", "broken"]) == 2
    assert "owner/name" in capsys.readouterr().err
