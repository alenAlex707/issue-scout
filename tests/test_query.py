import pytest

from issue_scout.query import build_query


def test_default_query():
    assert build_query() == "is:issue is:open no:assignee"


def test_complete_query():
    query = build_query(
        language="Python",
        labels=("good first issue", "help wanted"),
        repository="octo/demo",
        extra="comments:<5",
    )
    assert query == (
        'is:issue is:open no:assignee language:"Python" label:"good first issue" '
        'label:"help wanted" repo:octo/demo comments:<5'
    )


def test_include_assigned():
    assert "no:assignee" not in build_query(include_assigned=True)


def test_escaping():
    assert 'label:"say \\"hello\\""' in build_query(labels=('say "hello"',))


@pytest.mark.parametrize("repository", ["missing-slash", "/name", "owner/", "a/b/c"])
def test_invalid_repository(repository):
    with pytest.raises(ValueError, match="owner/name"):
        build_query(repository=repository)
