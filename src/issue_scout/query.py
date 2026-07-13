from __future__ import annotations


def build_query(
    *,
    language: str | None = None,
    labels: tuple[str, ...] = (),
    repository: str | None = None,
    include_assigned: bool = False,
    extra: str | None = None,
) -> str:
    """Build a GitHub search query from CLI filters."""
    parts = ["is:issue", "is:open"]
    if not include_assigned:
        parts.append("no:assignee")
    if language:
        parts.append(f'language:"{_escape(language)}"')
    for label in labels:
        parts.append(f'label:"{_escape(label)}"')
    if repository:
        _validate_repository(repository)
        parts.append(f"repo:{repository}")
    if extra:
        parts.append(extra.strip())
    return " ".join(parts)


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _validate_repository(value: str) -> None:
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("repository must use the 'owner/name' format")
