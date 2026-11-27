# issue.py: check a whole issue against every rule, using the checks in checks.py

from mailroom.checks import check_subject, check_preview, check_greeting, check_link, check_footer


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
