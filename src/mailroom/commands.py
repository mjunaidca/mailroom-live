# commands.py: the front door. The only module that reads the command line, reads today's date, or prints.

import sys
from datetime import date

from mailroom.subscribers import read_subscribers, count_emails, count_group, count_joined_since, next_send
from mailroom.issue import check_issue


def main() -> None:
    """Promise: run the command typed after `uv run mailroom`: subscribers, next-send or check."""
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


# Front door: only runs when this file is run directly, not when imported
if __name__ == "__main__":
    main()
