"""Central settings. Edit this file to tailor the assistants."""
import os

# Model
MODEL = os.getenv("ASSISTANT_MODEL", "llama3.1:8b")
NUM_CTX = 8192        # tokens the model can read at once (more = more RAM)
TEMPERATURE = 0       # 0 = consistent answers, higher = more varied

# Triage
MAX_CHARS = 12000     # longer messages are cut and flagged as truncated

# Draft Reply
DRAFT_TEMPERATURE = 0.5   # replies: a little variety, still professional

# Notes
NOTES_FILE = "notes.json"   # where notes are saved (not committed to git)
SUGGESTED_TAGS = [          # shown to the model; other tags are still allowed
    "preference",
    "decision",
    "deadline",
    "contact",
    "meeting",
    "todo",
    "reminder",             # only when no other type fits
]