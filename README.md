# AI Assistants

A collection of personal AI assistants that run **fully locally** using
[Ollama](https://ollama.com) and Python. No API keys, no usage costs.

## Status
Early development. Currently working:
- `triage` tool: classifies an incoming message as urgent / needs reply / fyi / ignore,
  with a summary and a suggested action (structured JSON output)

## Planned assistants
- **The Secretary**: gatekeeper and triage for incoming messages
- **The Intern**: research and file-summarizing tasks

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

## Usage
Run from the project root:
```
python -m tools.triage
```

## Configuration
All tunable settings live in [`config.py`](config.py):

| Setting | Default | What it does |
|---|---|---|
| `MODEL` | `llama3.1:8b` | Which Ollama model to use |
| `NUM_CTX` | `8192` | How many tokens the model can read at once (more uses more RAM) |
| `TEMPERATURE` | `0` | `0` gives consistent answers, higher gives more varied ones |
| `MAX_CHARS` | `12000` | Longer messages are cut and flagged as truncated |

To try a different model without editing the file, set the `ASSISTANT_MODEL` environment variable. In PowerShell:
```
$env:ASSISTANT_MODEL = "llama3.2:3b"
```
Make sure you've pulled the model first with `ollama pull <model>`.

## Project structure
```
tools/        reusable skills shared by all assistants
assistants/   (coming soon) each assistant's prompt, tools and loop
```

## License
This project is licensed under the [MIT License](LICENSE).