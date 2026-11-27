# checks.py: one check per rule in docs/email-rules.md


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
