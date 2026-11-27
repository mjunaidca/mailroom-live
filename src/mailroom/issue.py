# issue.py: what an Issue is, and building one from issue text.
# It imports nothing from checks.py: checks.py imports Issue from here, and one direction is enough.

from dataclasses import dataclass


@dataclass
class Issue:
    subject: str | None  # None: there was no Subject line. "": a Subject line with nothing after it
    preview: str | None  # None: there was no Preview line. "": a Preview line with nothing after it
    body: str  # every line except the Subject and Preview lines
    links: list[str]  # the url inside each [text](url), in order

    def personalize(self, first_name: str) -> Issue:
        """Promise: give back a NEW Issue with every {{first_name}} swapped for `first_name`; self is unchanged."""
        return Issue(
            fill_in(self.subject, first_name),
            fill_in(self.preview, first_name),
            self.body.replace("{{first_name}}", first_name),
            self.links,
        )


def fill_in(text: str | None, first_name: str) -> str | None:
    """Promise: give back `text` with every {{first_name}} swapped for `first_name`; None stays None."""
    if text is None:  # no line at all: nothing to fill in
        return None
    return text.replace("{{first_name}}", first_name)


def find_links(body: str) -> list[str]:
    """Promise: give back the url inside each [text](url), in the order they appear."""
    # Cut the body at every "](": each piece after a cut starts with a url, e.g. "https://...)\n\nSteep well,".
    # Keep the pieces that start with "http", and in each keep only what comes before the first ")".
    return [piece.split(")")[0] for piece in body.split("](") if piece.startswith("http")]


def parse_issue(text: str) -> Issue:
    """Promise: turn issue text into an Issue, with the Subject and Preview lines taken out of the body."""
    subject: str | None = None  # stays None if no line begins with "Subject:"
    preview: str | None = None  # stays None if no line begins with "Preview:"
    body: str = ""
    for line in text.splitlines():
        if line.startswith("Subject:"):
            subject = line.removeprefix("Subject:").strip()
        else:
            if line.startswith("Preview:"):
                preview = line.removeprefix("Preview:").strip()
            else:
                body = body + line + "\n"  # every other line belongs to the body, Enter put back
    return Issue(subject, preview, body, find_links(body))


def read_issue(path: str) -> Issue:
    """Promise: read the issue file at `path` and give it back as an Issue."""
    with open(path, encoding="utf-8") as f:
        text: str = f.read()
    return parse_issue(text)
