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


def check_subject(issue_text: str) -> list[str]:
    """Promise: give back the problems with the Subject line; [] means the subject is fine."""
    for line in issue_text.splitlines():
        if line.startswith("Subject:"):  # the line that begins with "Subject:"
            subject: str = line.removeprefix("Subject:").strip()  # the words after it, outer spaces removed
            if not subject:  # "" counts as "no": nothing left, or only spaces
                return ["empty"]
            if len(subject) > 50:  # the rule: 50 characters or fewer
                return ["too long"]
            return []
    return ["missing"]  # no line began with "Subject:"


def check_preview(issue_text: str) -> list[str]:
    """Promise: give back the problems with the Preview line; [] means the preview is fine."""
    for line in issue_text.splitlines():
        if line.startswith("Preview:"):  # the line that begins with "Preview:"
            preview: str = line.removeprefix("Preview:").strip()  # the words after it, outer spaces removed
            if not preview:  # "" counts as "no": nothing left, or only spaces
                return ["empty"]
            if len(preview) > 90:  # the rule: 90 characters or fewer
                return ["too long"]
            return []
    return ["missing"]  # no line began with "Preview:"


def check_greeting(issue_text: str) -> list[str]:
    """Promise: give back ["missing greeting"] unless the issue greets the reader with {{first_name}}."""
    if "{{first_name}}" in issue_text:  # `in`: does this text appear anywhere inside the issue?
        return []
    return ["missing greeting"]


def check_link(issue_text: str) -> list[str]:
    """Promise: give back the problem with the links; [] means there is exactly one link."""
    links: int = issue_text.count("](http")  # every [text](http://...) or [text](https://...) has "](http" once
    if links == 0:
        return ["no link"]
    if links > 1:
        return ["too many links"]
    return []


def check_footer(issue_text: str) -> list[str]:
    """Promise: give back ["missing footer"] unless both footer lines are there."""
    has_because: bool = False
    has_unsubscribe: bool = False
    for line in issue_text.splitlines():
        if line.startswith("You're getting this because"):
            has_because = True
        if "Unsubscribe: {{unsubscribe_url}}" in line:  # anywhere in the line, not only at the start
            has_unsubscribe = True
    if has_because and has_unsubscribe:
        return []
    return ["missing footer"]  # one problem, whether one footer line is missing or both


def check_issue(issue_text: str) -> list[str]:
    """Promise: give back every problem with the issue, in the order of docs/email-rules.md; [] means fine."""
    subject_problems: list[str] = ["subject " + problem for problem in check_subject(issue_text)]
    preview_problems: list[str] = ["preview " + problem for problem in check_preview(issue_text)]
    # `+` on lists joins them into one longer list, keeping the order
    return (
        subject_problems
        + preview_problems
        + check_greeting(issue_text)
        + check_link(issue_text)
        + check_footer(issue_text)
    )


# Front door: only runs for `uv run mailroom.py <name>`, not when imported
if __name__ == "__main__":
    command: str = sys.argv[1]  # "subscribers", "next-send" or "check"

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

    if command == "check":
        issue_path: str = sys.argv[2]  # the word after "check": which issue file to check
        problems: list[str] = check_issue(read_subscribers(issue_path))
        if problems:  # [] counts as "no": an empty list means no problems
            for problem in problems:
                print(problem)
            sys.exit(1)  # stop here and tell the terminal "failed" (exit code 1)
        print("OK")
        sys.exit(0)  # tell the terminal "passed" (exit code 0)
