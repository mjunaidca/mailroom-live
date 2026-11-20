# mailroom.py: tools for working with the subscribers file


def read_subscribers(path: str) -> str:
    """Promise: give back the whole file at `path` as one piece of text."""
    with open(path, encoding="utf-8") as f:
        text: str = f.read()
    return text


def count_emails(text: str) -> int:
    """Promise: count the subscriber rows (one email per row, header not counted)."""
    count: int = 0
    for line in text.splitlines():
        if line:  # skip empty lines ("" counts as "no")
            count += 1
    return count - 1  # the first line is the header, not an email


def count_group(text: str, group: str) -> int:
    """Promise: count the rows whose group column equals `group`."""
    count: int = 0
    for line in text.splitlines():
        columns: list[str] = line.split(",")
        if columns[3] == group:  # column 3 is "group"
            count += 1
    return count
