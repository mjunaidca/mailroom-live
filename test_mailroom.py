# test_mailroom.py: tests for the tools in mailroom.py
# Run with: uv run pytest
# pytest finds every function whose name starts with "test_" and runs it.
# A test passes if none of its asserts fail.

from mailroom import read_subscribers, count_emails, count_group, count_joined_since, next_send


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
