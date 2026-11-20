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
```
python tools/triage.py
```

## Project structure
```
tools/        reusable skills shared by all assistants
assistants/   (coming soon) each assistant's prompt, tools and loop
```

## License
This project is licensed under the [MIT License](LICENSE).