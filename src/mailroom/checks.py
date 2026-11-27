# checks.py: one check per rule in docs/email-rules.md, and check_issue to run them all in order.
# Every check takes an Issue (from issue.py), never raw text.

from mailroom.issue import Issue


def check_subject(issue: Issue) -> list[str]:
    """Promise: give back the problems with the Subject line; [] means the subject is fine."""
    if issue.subject is None:  # no line began with "Subject:"
        return ["missing"]
    if not issue.subject:  # "" counts as "no": a Subject line with nothing (or only spaces) after it
        return ["empty"]
    if len(issue.subject) > 50:  # the rule: 50 characters or fewer
        return ["too long"]
    return []


def check_preview(issue: Issue) -> list[str]:
    """Promise: give back the problems with the Preview line; [] means the preview is fine."""
    if issue.preview is None:  # no line began with "Preview:"
        return ["missing"]
    if not issue.preview:  # "" counts as "no": a Preview line with nothing (or only spaces) after it
        return ["empty"]
    if len(issue.preview) > 90:  # the rule: 90 characters or fewer
        return ["too long"]
    return []


def check_greeting(issue: Issue) -> list[str]:
    """Promise: give back ["missing greeting"] unless the body greets the reader with {{first_name}}."""
    if "{{first_name}}" in issue.body:  # `in`: does this text appear anywhere inside the body?
        return []
    return ["missing greeting"]


def check_link(issue: Issue) -> list[str]:
    """Promise: give back the problem with the links; [] means there is exactly one link."""
    links: int = len(issue.links)  # len() on a list: how many items are in it
    if links == 0:
        return ["no link"]
    if links > 1:
        return ["too many links"]
    return []


def check_footer(issue: Issue) -> list[str]:
    """Promise: give back ["missing footer"] unless both footer lines are there."""
    has_because: bool = False
    has_unsubscribe: bool = False
    for line in issue.body.splitlines():
        if line.startswith("You're getting this because"):
            has_because = True
        if "Unsubscribe: {{unsubscribe_url}}" in line:  # anywhere in the line, not only at the start
            has_unsubscribe = True
    if has_because and has_unsubscribe:
        return []
    return ["missing footer"]  # one problem, whether one footer line is missing or both


def check_issue(issue: Issue) -> list[str]:
    """Promise: give back every problem with the issue, in the order of docs/email-rules.md; [] means fine."""
    subject_problems: list[str] = ["subject " + problem for problem in check_subject(issue)]
    preview_problems: list[str] = ["preview " + problem for problem in check_preview(issue)]
    # `+` on lists joins them into one longer list, keeping the order
    return (
        subject_problems
        + preview_problems
        + check_greeting(issue)
        + check_link(issue)
        + check_footer(issue)
    )
