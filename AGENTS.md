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

### Not yet learned (teach first before using)

Anything not listed above, including: `if __name__ == "__main__":`, Python `import`, `len()`,
`elif`, f-strings, string methods (`.strip()`, `.split()`, …), tuples, sets, `try`/`except`,
reading files / CSV, dates, classes, `dataclass`, `pytest`, `input()`, `is None`, `range()`,
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

## 5. Project conventions

- Tooling: **uv**, Python **3.14** (see `.python-version`), **pyright in strict mode** (`pyproject.toml`).
- Every variable that needs it and every function has type labels (parameters and return type).
- Every function gets at least one hand-checkable `assert` of its promise.
- Money is stored as **whole cents in `int`** (e.g. $48.25 → `4825`). Convert to dollars only when printing.
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
