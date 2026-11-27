# subscribers.py: what a Subscriber is, reading them from a file, counting them, and working out dates

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Subscriber:
    first_name: str
    last_name: str
    email: str
    group: str  # "daily-drinkers", "gift-buyers" or "tea-curious"
    joined_on: date  # turned from text into a date once, when the file is read
    consent: str  # how they agreed to get email, e.g. "waitlist form"


def parse_row(line: str) -> Subscriber:
    """Promise: turn one CSV row into a Subscriber, its columns in the header's order."""
    columns: list[str] = line.split(",")
    return Subscriber(
        columns[0],  # first_name
        columns[1],  # last_name
        columns[2],  # email
        columns[3],  # group
        date.fromisoformat(columns[4]),  # joined_on
        columns[5],  # consent
    )


def parse_subscribers(text: str) -> list[Subscriber]:
    """Promise: turn CSV text into one Subscriber per row; the header row and empty lines are skipped."""
    return [parse_row(line) for line in text.splitlines() if line and not line.startswith("first_name,")]


def read_subscribers(path: str) -> list[Subscriber]:
    """Promise: read the CSV file at `path` and give back one Subscriber per row."""
    with open(path, encoding="utf-8") as f:
        text: str = f.read()
    return parse_subscribers(text)


def count_emails(subscribers: list[Subscriber]) -> int:
    """Promise: count the subscribers (one email each)."""
    return len(subscribers)


def count_group(subscribers: list[Subscriber], group: str) -> int:
    """Promise: count the subscribers whose group equals `group`."""
    count: int = 0
    for subscriber in subscribers:
        if subscriber.group == group:
            count += 1
    return count


def count_joined_since(subscribers: list[Subscriber], run_date: str, days: int) -> int:
    """Promise: count subscribers who joined in the last `days` days, from the cutoff up to the run date."""
    run: date = date.fromisoformat(run_date)
    cutoff: date = run - timedelta(days=days)
    count: int = 0
    for subscriber in subscribers:
        if cutoff <= subscriber.joined_on and subscriber.joined_on <= run:
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
