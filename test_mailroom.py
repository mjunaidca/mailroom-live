# test_mailroom.py: tests for the tools in the mailroom package (src/mailroom)
# Run with: uv run pytest
# pytest finds every function whose name starts with "test_" and runs it.
# A test passes if none of its asserts fail.

from datetime import date

from mailroom.subscribers import (
    Subscriber,
    parse_subscribers,
    read_subscribers,
    count_emails,
    count_group,
    count_joined_since,
    next_send,
)
from mailroom.checks import check_subject, check_issue
from mailroom.issue import Issue, parse_issue, read_issue


# Behavior 1: read_subscribers(path) gives back one Subscriber per row, every field in the right place.
# The learner decided this case and its answers. Never change an answer to make a test pass.
def test_the_first_subscriber_is_ayesha_khan() -> None:
    first: Subscriber = read_subscribers("data/subscribers.csv")[0]
    assert first.first_name == "Ayesha", "the first row's first_name is Ayesha"
    assert first.email == "ayesha.khan@example.com", "the first row's email is ayesha.khan@example.com"
    assert first.joined_on == date(2026, 9, 14), "the first row joined on 2026-09-14, read as a date"


# Behavior 2
def test_the_file_has_24_emails() -> None:
    subscribers: list[Subscriber] = read_subscribers("data/subscribers.csv")
    assert count_emails(subscribers) == 24, "there should be 24 emails"


# Behavior 3
def test_the_daily_drinkers_group_has_8_rows() -> None:
    subscribers: list[Subscriber] = read_subscribers("data/subscribers.csv")
    assert count_group(subscribers, "daily-drinkers") == 8, "daily-drinkers should have 8 rows"


# Behavior 5
def test_7_joined_in_the_30_days_before_2026_11_20() -> None:
    subscribers: list[Subscriber] = read_subscribers("data/subscribers.csv")
    assert count_joined_since(subscribers, "2026-11-20", 30) == 7, "7 should have joined in the last 30 days"


# Behavior 6: 30 days before 2026-11-20 is 2026-10-21: in. 2026-10-20: out.
def test_the_edge_day_counts_and_the_day_before_does_not() -> None:
    edge_rows: str = (
        "first_name,last_name,email,group,joined_on,consent\n"
        + "Amara,Diallo,amara.diallo@example.com,tea-curious,2026-10-21,waitlist form\n"
        + "Hiroshi,Tanaka,hiroshi.tanaka@example.com,daily-drinkers,2026-10-20,waitlist form\n"
    )
    assert count_joined_since(parse_subscribers(edge_rows), "2026-11-20", 30) == 1, "2026-10-21 counts, 2026-10-20 does not"


# Behavior 7
def test_a_join_after_the_run_date_does_not_count() -> None:
    late_rows: str = (
        "first_name,last_name,email,group,joined_on,consent\n"
        + "Zainab,Hussain,zainab.hussain@example.com,daily-drinkers,2026-11-03,waitlist form\n"
    )
    assert count_joined_since(parse_subscribers(late_rows), "2026-11-01", 30) == 0, "a join after the run date should not count"


# Behavior 8
def test_the_next_send_is_the_first_monday_of_next_month() -> None:
    assert next_send("2026-11-20") == "2026-12-07", "after 2026-11-20 the next send is 2026-12-07"
    assert next_send("2026-12-07") == "2027-01-04", "after 2026-12-07 the next send is 2027-01-04"


# Behavior 12: check_subject(issue) gives back a list of problems; [] means the subject is fine.
# The rule (docs/email-rules.md): the first line is `Subject: ...`, 50 characters or fewer.
# The learner decided these cases and their answers. Never change an answer to make a test pass.
def test_a_normal_subject_has_no_problems() -> None:
    issue: str = "Subject: The Steep Club opens Monday\nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == [], "a normal subject should have no problems"


def test_a_50_character_subject_has_no_problems() -> None:
    issue: str = "Subject: Your Steep Club box ships on Monday with new teas.\nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == [], "50 characters is allowed"


def test_a_51_character_subject_is_too_long() -> None:
    issue: str = "Subject: Your Steep Club box ships on Monday with fresh teas\nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == ["too long"], "51 characters is one too many"


# We count with len(), not by what a reader sees: a skin-tone emoji like 👍🏽 is a thumb plus a
# skin-tone dot, so it counts as 2. This subject looks like 49 characters but len() counts 51.
def test_a_skin_tone_emoji_counts_as_two_characters() -> None:
    issue: str = "Subject: 👍🏽 Your Steep Club box ships on Monday, new teas 👋🏽\nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == ["too long"], "each skin-tone emoji counts as 2, so this is 51"


def test_an_empty_subject_is_empty() -> None:
    issue: str = "Subject:\nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == ["empty"], "a subject with nothing in it is empty"


def test_a_subject_of_only_spaces_is_empty() -> None:
    issue: str = "Subject:     \nPreview: Your monthly tea box.\n"
    assert check_subject(parse_issue(issue)) == ["empty"], "a subject of only spaces counts as empty"


def test_no_subject_line_is_missing() -> None:
    issue: str = "Preview: Your monthly tea box.\n\nHi {{first_name}},\n"
    assert check_subject(parse_issue(issue)) == ["missing"], "an issue with no Subject line is missing its subject"


# Behavior 13: check_issue(issue) checks every rule in docs/email-rules.md and gives back
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


def make_issue(preview: str, greeting: str, links: str, footer: str) -> Issue:
    """Promise: put the pieces together into one Issue, a blank line between each part."""
    text: str = SUBJECT + "\n" + preview + "\n\n" + greeting + "\n\n" + links + "\n\n" + SIGN_OFF + "\n\n" + footer + "\n"
    return parse_issue(text)


def test_issue_01_has_no_problems() -> None:
    issue: Issue = read_issue("issues/issue-01.md")
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
    issue: Issue = make_issue(PREVIEW, "Hi there,", ONE_LINK, FOOTER)
    assert check_issue(issue) == ["missing greeting"], "the greeting must use {{first_name}}"


def test_two_links_are_too_many_even_when_one_is_http() -> None:
    links: str = ONE_LINK + " or [see the teas](http://kettlebird.example/teas)"  # two links on one line
    assert check_issue(make_issue(PREVIEW, GREETING, links, FOOTER)) == ["too many links"], "exactly one link"


def test_no_link_at_all_is_no_link() -> None:
    issue: Issue = make_issue(PREVIEW, GREETING, "Visit our shop soon.", FOOTER)
    assert check_issue(issue) == ["no link"], "exactly one link: zero is not enough"


def test_only_one_footer_line_is_a_missing_footer() -> None:
    footer: str = "You're getting this because you joined the Kettlebird Tea waitlist."
    assert check_issue(make_issue(PREVIEW, GREETING, ONE_LINK, footer)) == ["missing footer"], "both lines needed"


def test_no_footer_and_no_greeting_are_two_problems() -> None:
    issue: Issue = make_issue(PREVIEW, "Hello,", ONE_LINK, "")
    assert check_issue(issue) == ["missing greeting", "missing footer"], "two problems, in rule order"


# Behavior 16: read_issue(path) gives back an Issue; its links are the URLs inside [text](url).
# Behavior 17: issue.personalize(first_name) gives back a new Issue with the first name swapped in.
# The learner decided these cases and their answers. Never change an answer to make a test pass.
def test_issue_01_has_one_link_to_the_steep_club() -> None:
    issue: Issue = read_issue("issues/issue-01.md")
    assert issue.links == ["https://kettlebird.example/steep-club"], "issue-01.md has exactly this one link"


def test_personalize_puts_the_first_name_where_the_placeholder_was() -> None:
    ayesha: Issue = read_issue("issues/issue-01.md").personalize("Ayesha")
    assert "Hi Ayesha," in ayesha.body, "{{first_name}} becomes Ayesha"
    assert not "{{first_name}}" in ayesha.body, "no {{first_name}} is left over"


def test_personalize_leaves_the_unsubscribe_url_as_it_is() -> None:
    ayesha: Issue = read_issue("issues/issue-01.md").personalize("Ayesha")
    assert "Unsubscribe: {{unsubscribe_url}}" in ayesha.body, "{{unsubscribe_url}} is not touched"


def test_personalize_leaves_the_original_issue_unchanged() -> None:
    issue: Issue = read_issue("issues/issue-01.md")
    issue.personalize("Ayesha")
    assert "Hi {{first_name}}," in issue.body, "the original keeps {{first_name}}, so Tom's copy comes out clean"


# Behaviors still checked by hand (they need the command line, not a function):
#
# Behavior 4: `uv run mailroom subscribers` reads data/subscribers.csv and prints exactly:
#
#   24 emails
#   daily-drinkers: 8
#   gift-buyers: 8
#   tea-curious: 8
#
# Behavior 9: `uv run mailroom subscribers --since-days 30 --run-date 2026-11-20`
# prints the four lines above, then:
#
#   7 joined in the last 30 days
#
# Behavior 10: `uv run mailroom next-send --run-date 2026-11-20` prints exactly:
#
#   next send: 2026-12-07
#
# Behavior 11: leave out --run-date and both commands use today's date.
# Only the commands module (`main()` in src/mailroom/commands.py) may read today's date.
#
# Behavior 14: `uv run mailroom check issues/issue-01.md` prints exactly `OK`,
# and `echo $?` right after it prints `0`.
#
# Behavior 15: `uv run mailroom check <a broken issue file>` prints each problem on its
# own line (the same words check_issue gives back, in the same order), and `echo $?` prints `1`.
