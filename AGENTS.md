# AGENTS.md — mailroom-live

Everything an AI agent needs to know before touching this repo. Read it fully, every session.

## 1. What this project is

`mailroom-live` is a **learning project**. The learner is working through
*Programming Fundamentals in the AI Era* (The AI Agent Factory, Part III, Chapter 13):
<https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/>

The goal is not to ship features fast. The goal is that **the learner understands every line**.
The agent writes code; the learner reads, predicts, checks and directs.

- Language: **Python only** (the chapter also teaches TypeScript; this repo does not use it).
- Domain: a "mailroom": features are decided together with the learner, one small step at a time.

### The lab we follow: Mailroom Lab

<https://claude.ai/artifact/KHyQVY95yEYdSZQgueA5Fi>

This is the step-by-step track for the project: 27 steps (0 to 26) across Chapters 13 to 15,
grouped as 0 The base · A Read and check · B Shape the code · C Talk to a service ·
D Ship like a team · E Into your studio. Each step names its lesson, the problem, what the learner
decides first, what their prompt must say, Investigate/Modify tasks, and a fresh-session Check.

- The learner writes their own prompts; the lab's sample prompts are only for comparison afterwards.
- The lab's practice files (`subscribers.csv`, `issue-01.md`, `email-rules.md`, `new-signups.csv`)
  are made-up data. No real emails are ever sent.
- If the lab and this file disagree (for example the concept boundary in §3), **this file wins**.

## 2. Where the learner is

**Completed: up to and including lesson 13.7.** Update this line whenever the learner finishes a lesson.

| Lesson | Title |
| --- | --- |
| 13.1 | You read, the agent writes |
| 13.2 | The workbench |
| 13.3 | Values, types and variables |
| 13.4 | Decisions and repetition |
| 13.5 | Two conditions, empty values and while loops |
| 13.6 | Functions: the signature is the contract |
| 13.7 | Lists and dictionaries |

Coming next (NOT yet learned): 13.8 Text from a file · 13.9 Dates · 13.10 Reading an error ·
13.11 Tests first: the TDG loop · 13.12 Judgment · 13.13 How today's tools realize it · Lab 13.

## 3. The concept boundary (most important rule)

**Only use Python features the learner has already learned.** If a task needs anything new,
STOP and **teach the concept first** (see §4), then use it. Never slip a new feature in silently.

### Allowed (learned in 13.1–13.7)

- Values and variables: `name = value`, reassignment, `#` comments, `print(a, b)`
- Types: `str`, `int`, `float` (never for money), `bool` (`True`/`False`), `None`
- Type labels on variables and functions: `x: int = 5`, `def f(a: int) -> int:`
- Conversion: `int(text)` (and that `int("4,825.00")` raises `ValueError`)
- `+` on text joins, on numbers adds, mixed raises `TypeError`
- `if` / `else`, comparisons `== > >= < <=`, logical `and` `or` `not`
- Truthiness traps: `""`, `None` and `0` all count as "no"; default idiom `x = x or "default"`
- Loops: `for x in items:`, `while condition:` (with a line that changes the condition), `x += 1`
- Filter pattern (`if` inside a loop) and list comprehension `[x for x in items if ...]`
- Functions: parameters, arguments, body, `return`, signature as contract, pure/deterministic functions
- `assert condition, "message"` as a hand-checkable test of a function's promise
- Lists: literals, 0-based indexing, `IndexError` when out of range
- Dictionaries: `dict[str, str]` etc., `d["key"]`, `KeyError`, `.get(key)`, `.get(key, default)`,
  case-sensitive keys, records (a dict with named fields, accessed as `inv["status"]`)
- Sorting: `sorted(items)`, `key=`, `key=lambda r: r["cents"]`, `reverse=True`
- Workbench: `uv run python file.py`, `uv run pyright` (strict mode)

### Taught early (ahead of 13.8, via PRIMM in this repo)

- Reading a file: `with open(path, encoding="utf-8") as f:` then `text = f.read()` gives one `str`
- Newline `\n`: the invisible "Enter" between lines; `print` obeys it rather than showing it
- `text.splitlines()` → `list[str]`, one item per line, `\n` removed
- `row.split(",")` → `list[str]` of columns, the commas removed
- `from mailroom import name` to use another file's function; without it → `NameError`
- `import sys` (plain form, use with a dot) and `sys.argv`: the typed command words as a list,
  `[0]` is the file name, `[1]` the first word after it
- `if __name__ == "__main__":` front door: runs only when the file is run directly, not imported

### Taught early (ahead of 13.9, via PRIMM in this repo)

- `from datetime import date, timedelta`; a `date` is a calendar square, text is only a picture of it
- `date.fromisoformat("2026-11-20")` text → date; `day.isoformat()` date → text
- `day - timedelta(days=30)` / `day + timedelta(days=1)`: steps, the start day is not counted
- Comparing dates with `<=` etc.; `date + "text"` raises `TypeError`
- `day.weekday()`: Monday is `0` … Sunday is `6`; step with `while not day.weekday() == 0:`
- `day.year`, `day.month` as `int`; `date(year, month, 1)` builds a date; month 13 rolls to 1, year + 1

### Not yet learned (teach first before using)

Anything not listed above, including: `len()`,
`elif`, f-strings, other string methods (`.strip()`, …), slicing, `isinstance()`, tuples, sets, `try`/`except`,
the `csv` module, dates, classes, `dataclass`, `pytest`, `input()`, `is None`, `range()`,
`enumerate()`, list methods like `.append()`, `match`, async, external packages.

When in doubt whether something was taught: **ask the learner**, don't assume.

## 4. How we learn: PRIMM-AI+

Every new piece of code moves through five steps. The learner drives; the agent assists.

| Step | Learner does | Agent does |
| --- | --- | --- |
| **P**redict | Writes down what the code will do *before* it runs | Stays quiet. The guess is theirs |
| **R**un | Approves the run, sees the real output | Runs it (with permission) |
| **I**nvestigate | Compares guess vs. output, asks *why* | Explains a line only when asked |
| **M**odify | Changes one thing, predicts again, runs again | Makes the edit described |
| **M**ake | Specifies their own version | Builds against that spec; learner verifies |

**AI+** means: the agent is always available as a reading partner, and **nothing is accepted on
faith**: a run or a test decides, not the agent's word.

Rules for the agent:

1. **Predict before run, every time.** Show the code, ask for a prediction, wait. Never show
   output first. "A guess made after the output is not a guess."
2. **Teaching a new concept** (outside §3's allowed list): give one plain analogy, a tiny
   example, then run a PRIMM cycle on it *before* using it in project code. Then add it to the
   allowed list in §3.
3. One small step per turn. Don't dump large files on the learner.
4. Don't explain unless asked during Predict/Run. Explain line by line during Investigate.
5. Never accept totals, dates or amounts a model "worked out" in chat: write a function plus an
   `assert`, and run it.
6. **When something breaks, show the full error first.** Paste the complete output exactly as
   printed (traceback and all, not a summary) *before* changing any code or data. The learner
   reads it first; fixes come after.

## 5. Project conventions

- Tooling: **uv**, Python **3.14** (see `.python-version`), **pyright in strict mode** (`pyproject.toml`).
- Every variable that needs it and every function has type labels (parameters and return type).
- Every function gets at least one hand-checkable `assert` of its promise.
- Money is stored as **whole cents in `int`** (e.g. $48.25 → `4825`). Convert to dollars only when printing.
- **Never read today's date inside the logic. Pass the run date in.** Functions take the run date
  as a parameter (e.g. `next_send(run_date: str) -> str`), so the same input always gives the same
  output and a check can pin any day. Only the command line (the `if __name__ == "__main__":` front
  door) may read today's date, and only when `--run-date` is left out.
- Dates as year-first text (`"2027-03-05"`) until 13.9 teaches dates properly.
- Keep it simple: plain functions, lists and dicts. No classes or libraries until taught.

Commands:

```bash
uv run python main.py   # run
uv run pyright          # type check: must show 0 errors before any commit
```

## 6. Git workflow

- Remote: GitHub `mjunaidca/mailroom-live`, branch `main`.
- Before committing: run the file and `uv run pyright`; both must pass.
- Small commits with clear messages. Show `git status` / `git diff` to the learner before committing.
- Ask before pushing.
