# test_mailroom.py: tests for the tools in mailroom.py
# Run with: uv run pytest
# pytest finds every function whose name starts with "test_" and runs it.
# A test passes if none of its asserts fail.

from mailroom import (
    read_subscribers,
    count_emails,
    count_group,
    count_joined_since,
    next_send,
    check_subject,
    check_issue,
)


# Behavior 1
def test_reading_the_file_gives_back_text() -> None:
    subscribers: str = read_subscribers("data/subscribers.csv")
    assert isinstance(subscribers, str), "reading the file should give back text (str)"


# Behavior 2
def test_the_file_has_24_emails() -> None:
    subscribers: str = read_subscribers("data/subscribers.csv")
    assert count_emails(subscribers) == 24, "there should be 24 emails"


# Behavior 3
def test_the_daily_drinkers_group_has_8_rows() -> None:
    subscribers: str = read_subscribers("data/subscribers.csv")
    assert count_group(subscribers, "daily-drinkers") == 8, "daily-drinkers should have 8 rows"


# Behavior 5
def test_7_joined_in_the_30_days_before_2026_11_20() -> None:
    subscribers: str = read_subscribers("data/subscribers.csv")
    assert count_joined_since(subscribers, "2026-11-20", 30) == 7, "7 should have joined in the last 30 days"


# Behavior 6: 30 days before 2026-11-20 is 2026-10-21: in. 2026-10-20: out.
def test_the_edge_day_counts_and_the_day_before_does_not() -> None:
    edge_rows: str = (
        "first_name,last_name,email,group,joined_on,consent\n"
        + "Amara,Diallo,amara.diallo@example.com,tea-curious,2026-10-21,waitlist form\n"
        + "Hiroshi,Tanaka,hiroshi.tanaka@example.com,daily-drinkers,2026-10-20,waitlist form\n"
    )
    assert count_joined_since(edge_rows, "2026-11-20", 30) == 1, "2026-10-21 counts, 2026-10-20 does not"


# Behavior 7
def test_a_join_after_the_run_date_does_not_count() -> None:
    late_rows: str = (
        "first_name,last_name,email,group,joined_on,consent\n"
        + "Zainab,Hussain,zainab.hussain@example.com,daily-drinkers,2026-11-03,waitlist form\n"
    )
    assert count_joined_since(late_rows, "2026-11-01", 30) == 0, "a join after the run date should not count"


# Behavior 8
def test_the_next_send_is_the_first_monday_of_next_month() -> None:
    assert next_send("2026-11-20") == "2026-12-07", "after 2026-11-20 the next send is 2026-12-07"
    assert next_send("2026-12-07") == "2027-01-04", "after 2026-12-07 the next send is 2027-01-04"


# Behavior 12: check_subject(issue_text) gives back a list of problems; [] means the subject is fine.
# The rule (docs/email-rules.md): the first line is `Subject: ...`, 50 characters or fewer.
# The learner decided these cases and their answers. Never change an answer to make a test pass.
def test_a_normal_subject_has_no_problems() -> None:
    issue: str = "Subject: The Steep Club opens Monday\nPreview: Your monthly tea box.\n"
    assert check_subject(issue) == [], "a normal subject should have no problems"


def test_a_50_character_subject_has_no_problems() -> None:
    issue: str = "Subject: Your Steep Club box ships on Monday with new teas.\nPreview: Your monthly tea box.\n"
    assert check_subject(issue) == [], "50 characters is allowed"


def test_a_51_character_subject_is_too_long() -> None:
    issue: str = "Subject: Your Steep Club box ships on Monday with fresh teas\nPreview: Your monthly tea box.\n"
    assert check_subject(issue) == ["too long"], "51 characters is one too many"


def test_an_empty_subject_is_empty() -> None:
    issue: str = "Subject:\nPreview: Your monthly tea box.\n"
    assert check_subject(issue) == ["empty"], "a subject with nothing in it is empty"


def test_a_subject_of_only_spaces_is_empty() -> None:
    issue: str = "Subject:     \nPreview: Your monthly tea box.\n"
    assert check_subject(issue) == ["empty"], "a subject of only spaces counts as empty"


def test_no_subject_line_is_missing() -> None:
    issue: str = "Preview: Your monthly tea box.\n\nHi {{first_name}},\n"
    assert check_subject(issue) == ["missing"], "an issue with no Subject line is missing its subject"


# Behavior 13: check_issue(issue_text) checks every rule in docs/email-rules.md and gives back
# all the problems, in the order the rules are written; [] means the issue is fine.
# The learner decided these cases and their answers. Never change an answer to make a test pass.

# The good pieces of an issue. Each test swaps in one broken piece to see one problem.
SUBJECT: str = "Subject: The Steep Club opens Monday"
PREVIEW: str = "Preview: Your monthly tea box, chosen by our blenders."
GREETING: str = "Hi {{first_name}},"
ONE_LINK: str = "[Join The Steep Club](https://kettlebird.example/steep-club)"
SIGN_OFF: str = "Steep well,\nThe Kettlebird Tea team"
FOOTER: str = (
    "You're getting this because you joined the Kettlebird Tea waitlist.\n"
    + "Kettlebird Tea, {{company_address}} · Unsubscribe: {{unsubscribe_url}}"
)


def make_issue(preview: str, greeting: str, links: str, footer: str) -> str:
    """Promise: put the pieces together into one issue, a blank line between each part."""
    return SUBJECT + "\n" + preview + "\n\n" + greeting + "\n\n" + links + "\n\n" + SIGN_OFF + "\n\n" + footer + "\n"


def test_issue_01_has_no_problems() -> None:
    issue: str = read_subscribers("issues/issue-01.md")  # read_subscribers reads any file as text
    assert check_issue(issue) == [], "issue-01.md follows every rule"


def test_a_90_character_preview_has_no_problems() -> None:
    preview: str = "Preview: Your monthly tea box, chosen by our blenders. Founding members get the first box for free."
    assert check_issue(make_issue(preview, GREETING, ONE_LINK, FOOTER)) == [], "90 characters is allowed"


def test_a_91_character_preview_is_too_long() -> None:
    preview: str = "Preview: Your monthly tea box, chosen by our blenders. Founding members get the first box for free!!"
    assert check_issue(make_issue(preview, GREETING, ONE_LINK, FOOTER)) == ["preview too long"], "91 is one too many"


def test_an_empty_preview_is_empty() -> None:
    assert check_issue(make_issue("Preview:", GREETING, ONE_LINK, FOOTER)) == ["preview empty"], "nothing after Preview:"


def test_no_preview_line_is_missing() -> None:
    assert check_issue(make_issue("", GREETING, ONE_LINK, FOOTER)) == ["preview missing"], "no line starts Preview:"


def test_no_first_name_is_a_missing_greeting() -> None:
    issue: str = make_issue(PREVIEW, "Hi there,", ONE_LINK, FOOTER)
    assert check_issue(issue) == ["missing greeting"], "the greeting must use {{first_name}}"


def test_two_links_are_too_many_even_when_one_is_http() -> None:
    links: str = ONE_LINK + " or [see the teas](http://kettlebird.example/teas)"  # two links on one line
    assert check_issue(make_issue(PREVIEW, GREETING, links, FOOTER)) == ["too many links"], "exactly one link"


def test_no_link_at_all_is_no_link() -> None:
    issue: str = make_issue(PREVIEW, GREETING, "Visit our shop soon.", FOOTER)
    assert check_issue(issue) == ["no link"], "exactly one link: zero is not enough"


def test_only_one_footer_line_is_a_missing_footer() -> None:
    footer: str = "You're getting this because you joined the Kettlebird Tea waitlist."
    assert check_issue(make_issue(PREVIEW, GREETING, ONE_LINK, footer)) == ["missing footer"], "both lines needed"


def test_no_footer_and_no_greeting_are_two_problems() -> None:
    issue: str = make_issue(PREVIEW, "Hello,", ONE_LINK, "")
    assert check_issue(issue) == ["missing greeting", "missing footer"], "two problems, in rule order"


# Behaviors still checked by hand (they need the command line, not a function):
#
# Behavior 4: `uv run mailroom.py subscribers` reads data/subscribers.csv and prints exactly:
#
#   24 emails
#   daily-drinkers: 8
#   gift-buyers: 8
#   tea-curious: 8
#
# Behavior 9: `uv run mailroom.py subscribers --since-days 30 --run-date 2026-11-20`
# prints the four lines above, then:
#
#   7 joined in the last 30 days
#
# Behavior 10: `uv run mailroom.py next-send --run-date 2026-11-20` prints exactly:
#
#   next send: 2026-12-07
#
# Behavior 11: leave out --run-date and both commands use today's date.
# Only the front door (`if __name__ == "__main__":`) may read today's date.
#
# Behavior 14: `uv run mailroom.py check issues/issue-01.md` prints exactly `OK`,
# and `echo $?` right after it prints `0`.
#
# Behavior 15: `uv run mailroom.py check <a broken issue file>` prints each problem on its
# own line (the same words check_issue gives back, in the same order), and `echo $?` prints `1`.
