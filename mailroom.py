# mailroom.py: tools for working with the subscribers file

import sys
from datetime import date, timedelta


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


def count_joined_since(text: str, run_date: str, days: int) -> int:
    """Promise: count rows that joined in the last `days` days, from the cutoff up to the run date."""
    run: date = date.fromisoformat(run_date)
    cutoff: date = run - timedelta(days=days)
    count: int = 0
    for line in text.splitlines():
        columns: list[str] = line.split(",")
        if not columns[4] == "joined_on":  # column 4 is "joined_on"; skip the header row
            joined: date = date.fromisoformat(columns[4])
            if cutoff <= joined and joined <= run:
                count += 1
    return count


def next_send(run_date: str) -> str:
    """Promise: give back the first Monday of the month after `run_date`, as "YYYY-MM-DD" text."""
    run: date = date.fromisoformat(run_date)
    year: int = run.year
    month: int = run.month + 1
    if month == 13:  # no month 13: roll over to January of next year
        month = 1
        year = year + 1
    day: date = date(year, month, 1)
    while not day.weekday() == 0:  # step forward until Monday (0)
        day = day + timedelta(days=1)
    return day.isoformat()


# Front door: only runs for `uv run mailroom.py <name>`, not when imported
if __name__ == "__main__":
    command: str = sys.argv[1]  # "subscribers" or "next-send"

    # Options: the word right AFTER "--run-date" is the date, right AFTER "--since-days" is the days
    run_date: str = ""
    since_days: str = ""
    previous: str = ""
    for word in sys.argv:
        if previous == "--run-date":
            run_date = word
        if previous == "--since-days":
            since_days = word
        previous = word

    # The ONLY place today's date is read, and only when --run-date was left out
    run_date = run_date or date.today().isoformat()

    if command == "subscribers":
        text: str = read_subscribers("data/subscribers.csv")
        print(count_emails(text), "emails")
        groups: list[str] = ["daily-drinkers", "gift-buyers", "tea-curious"]
        for group in groups:
            print(group + ":", count_group(text, group))
        if since_days:  # "" counts as "no": only when --since-days was given
            days: int = int(since_days)
            print(count_joined_since(text, run_date, days), "joined in the last", days, "days")

    if command == "next-send":
        print("next send:", next_send(run_date))
