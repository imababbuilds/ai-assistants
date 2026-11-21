# AI Assistants

A collection of personal AI assistants that run **fully locally** using
[Ollama](https://ollama.com) and Python. No API keys, no usage costs.

## Status
Early development. There's no assistant to run yet. These building blocks are working and covered by the test suite:
- `triage`: classifies an incoming message as urgent / needs reply / fyi / ignore, with a summary and a suggested action (structured JSON output)
- `draft_reply`: drafts a reply to a message as a structured `Draft` (subject, body, and a `needs_review` flag that is set when the draft contains `[placeholders]` the user must fill in). An optional `instructions` argument lets you say what the reply should convey
- Notes tools, stored in one shared local file:
  - `save_note`: saves a note (text, tags, which assistant saved it) and skips exact duplicates
  - `complete_note`, `supersede_note`, `delete_note`: mark a note done or out of date, or delete it (deleting needs the boss's approval)
  - `check_conflicts`: flags notes that contradict or replace another note, for the boss to review

## Planned assistants
Each assistant has its own personality and tools, built on a shared core.

### Front office

#### The Secretary
Manages the boss's inbox, time and communications.
- [x] Triage incoming messages (urgent / needs reply / FYI / ignore)
- [x] Draft replies
- [ ] Read reports and brief the boss, summarizing them and flagging anything that needs attention
- [ ] Send emails and messages (after the boss approves the draft)
- [ ] Set and manage reminders
- [ ] Manage the calendar: schedule, confirm and reschedule meetings
- [ ] Reach out to people to confirm or coordinate (stretch goal)

#### The Scribe
Turns meetings into clear records and follow-ups.
- [ ] Turn meeting notes or transcripts into minutes with a short summary
- [ ] Extract decisions and action items, with owners and due dates when mentioned
- [ ] File action items as work items
- [ ] Save meeting notes and search past ones

### Projects
Work items can be created in GitHub Issues or Azure DevOps (set in `config.py`, access tokens in `.env`).

#### The Researcher
Gathers what a decision needs, from sources you can check.
- [ ] Take a goal ("find a better way to do X", "an alternative to A for B") and research options
- [ ] Report pros, cons and limitations for each option, with sources cited
- [ ] After the user approves an option, hand off to the Project Manager to turn it into a project plan with a proposed timeline

#### The Project Manager
Turns approved ideas into plans and keeps them on track.
- [ ] Write project proposals and plans with ordered tasks and a proposed timeline
- [ ] Track progress from work items and report status, overdue items and blockers

#### The Intern
Takes on tedious setup work, following instructions.
- [ ] Scaffold new projects (for example, an empty API project) from a template describing the company's folder structure and naming conventions
- [ ] Create work items in order from an existing project plan, ready to assign

#### The Debugger
Reviews code, finds problems and reports them.
- [ ] Find bugs and file them as work items with reproduction steps and relevant context
- [ ] Suggest improvements and file them as work items

### Data and finance

#### The Bookkeeper
Keeps financial records accurate and organized.
- [ ] Extract details from receipts and invoices (vendor, date, amount, category)
- [ ] Categorize expenses and check that totals add up
- [ ] Prepare expense reports

#### The Analyst
Digs into data and answers questions about it.
- [ ] Answer questions about spreadsheets and CSV files, with calculations done in code so the numbers are exact
- [ ] Find trends and outliers and explain them in plain language
- [ ] Produce a written analysis on request

### People

#### The Mentor
Helps new hires get up to speed on how the office works.
- [ ] Answer questions about the company's workflows and standards, based on the company's own documents
- [ ] Give newcomers templates for common tasks, naming conventions and file organization
- [ ] Spot where a described situation deviates from or breaks the documented workflow

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/download) with the `llama3.1:8b` model
- 16 GB RAM recommended

## Setup
```
ollama pull llama3.1:8b
git clone https://github.com/imababbuilds/ai-assistants.git
cd ai-assistants
python -m venv .venv
.venv\Scripts\activate      # Mac/Linux: source .venv/bin/activate
pip install ollama
```

## Tests
```
pip install pytest
pytest              # fast tests, no model needed
pytest -m llm       # tests that call the model (slower)
```

## Configuration
All tunable settings live in [`config.py`](config.py):

| Setting | Default | What it does |
|---|---|---|
| `MODEL` | `llama3.1:8b` | Which Ollama model to use |
| `NUM_CTX` | `8192` | How many tokens the model can read at once (more uses more RAM) |
| `TEMPERATURE` | `0` | `0` gives consistent answers, higher gives more varied ones |
| `DRAFT_TEMPERATURE` | `0.5` | Variety in drafted replies, so regenerating gives a different draft |
| `MAX_CHARS` | `12000` | Longer messages are cut and flagged as truncated |
| `NOTES_FILE` | `data/notes.json` | Where saved notes are stored (not committed to git) |
| `SUGGESTED_TAGS` | `preference`, `todo`, `reminder`, `info` | Tags the assistants are nudged to use on notes. Other tags are still allowed |

To try a different model without editing the file, set the `ASSISTANT_MODEL` environment variable. In PowerShell:
```
$env:ASSISTANT_MODEL = "llama3.2:3b"
```
Make sure you've pulled the model first with `ollama pull <model>`.

## Project structure
```
config.py          settings shared by all assistants
tools/             reusable skills shared by all assistants
  messages/        triage, draft_reply
  notes/           store, save_note, manage_notes
tests/             automated tests
data/              files created while running (not committed)
assistants/        (coming soon) each assistant's prompt, tools and loop
```

## License
This project is licensed under the [MIT License](LICENSE).