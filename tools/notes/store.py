import json
from pathlib import Path
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from config import NOTES_FILE


class Note(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    text: str
    created: str
    tags: list[str] = []
    source: str = "unknown"  # which assistant saved the note
    status: Literal["open", "done", "superseded"] = "open"


def load_notes() -> list[Note]:
    path = Path(NOTES_FILE)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Note(**item) for item in data]


def write_notes(notes: list[Note]) -> None:
    path = Path(NOTES_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([n.model_dump() for n in notes], indent=2),
        encoding="utf-8",
    )


def find_note(notes: list[Note], note_id: str) -> Note:
    for note in notes:
        if note.id == note_id:
            return note
    raise ValueError(f"No note with id '{note_id}'.")