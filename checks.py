# checks.py: tests for the tools in mailroom.py

from mailroom import read_subscribers, count_emails, count_group, count_joined_since, next_send

subscribers: str = read_subscribers("data/subscribers.csv")

# Behavior 1: when the file is read, its output type is string
assert isinstance(subscribers, str), "reading the file should give back text (str)"

# Behavior 2: total number of emails is 24
assert count_emails(subscribers) == 24, "there should be 24 emails"

# Behavior 3: the daily-drinkers group has 8 rows
assert count_group(subscribers, "daily-drinkers") == 8, "daily-drinkers should have 8 rows"

# Behavior 5: with the run date 2026-11-20, 7 subscribers joined in the last 30 days
assert count_joined_since(subscribers, "2026-11-20", 30) == 7, "7 should have joined in the last 30 days"

# Behavior 6: the edge day counts. 30 days before 2026-11-20 is 2026-10-21: in. 2026-10-20: out.
edge_rows: str = (
    "first_name,last_name,email,group,joined_on,consent\n"
    + "Amara,Diallo,amara.diallo@example.com,tea-curious,2026-10-21,waitlist form\n"
    + "Hiroshi,Tanaka,hiroshi.tanaka@example.com,daily-drinkers,2026-10-20,waitlist form\n"
)
assert count_joined_since(edge_rows, "2026-11-20", 30) == 1, "2026-10-21 counts, 2026-10-20 does not"

# Behavior 7: someone who joined AFTER the run date does not count
late_rows: str = (
    "first_name,last_name,email,group,joined_on,consent\n"
    + "Zainab,Hussain,zainab.hussain@example.com,daily-drinkers,2026-11-03,waitlist form\n"
)
assert count_joined_since(late_rows, "2026-11-01", 30) == 0, "a join after the run date should not count"

# Behavior 8: the next send is the first Monday of the NEXT month
assert next_send("2026-11-20") == "2026-12-07", "after 2026-11-20 the next send is 2026-12-07"
assert next_send("2026-12-07") == "2027-01-04", "after 2026-12-07 the next send is 2027-01-04"

print("all checks passed")

# Behavior 4 (written before the code, checked by hand for now):
# `uv run mailroom.py subscribers` reads data/subscribers.csv and prints exactly:
#
#   24 emails
#   daily-drinkers: 8
#   gift-buyers: 8
#   tea-curious: 8
#
# Behavior 9 (checked by hand):
# `uv run mailroom.py subscribers --since-days 30 --run-date 2026-11-20` prints the four lines above, then:
#
#   7 joined in the last 30 days
#
# Behavior 10 (checked by hand):
# `uv run mailroom.py next-send --run-date 2026-11-20` prints exactly:
#
#   next send: 2026-12-07
#
# Behavior 11 (checked by hand): leave out --run-date and both commands use today's date.
# Only the front door (`if __name__ == "__main__":`) may read today's date.
