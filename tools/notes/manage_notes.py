import ollama
from pydantic import BaseModel

from config import MODEL, NUM_CTX, SUGGESTED_TAGS, TEMPERATURE
from tools.notes.store import Note, find_note, load_notes, write_notes

MAX_COMPARE = 20  # compare against at most this many recent notes

CONFLICT_PROMPT = """You compare a new note against existing notes about the same subject.

List an existing note ONLY if the new note contradicts it or makes it out of date
(for example, a changed preference, or a new date replacing an old one).
Notes that are merely related, or that say the same thing, are NOT conflicts.

For each conflict, give the existing note's id and a short reason.
If there are no conflicts, return an empty list.
Only use ids from the list you are given."""


class Conflict(BaseModel):
    note_id: str
    reason: str


class ConflictReport(BaseModel):
    conflicts: list[Conflict] = []


def complete_note(note_id: str) -> Note:
    """Mark a note (usually a todo) as done. The note is kept, not deleted.

    Args:
        note_id: The id of the note to complete.
    """
    notes = load_notes()
    note = find_note(notes, note_id)
    note.status = "done"
    write_notes(notes)
    return note


def supersede_note(note_id: str) -> Note:
    """Mark a note as out of date because a newer note replaces it. The note is kept.

    Only call this after the boss has confirmed the old note is out of date.

    Args:
        note_id: The id of the old note.
    """
    notes = load_notes()
    note = find_note(notes, note_id)
    note.status = "superseded"
    write_notes(notes)
    return note


def delete_note(note_id: str) -> Note:
    """Permanently delete a note. This cannot be undone.

    Only call this after the boss has explicitly approved the deletion.

    Args:
        note_id: The id of the note to delete.
    """
    notes = load_notes()
    note = find_note(notes, note_id)
    write_notes([n for n in notes if n.id != note_id])
    return note


def _subject_tags(note: Note) -> set[str]:
    """Tags about who or what the note concerns, not the type tags like 'todo'."""
    return {t for t in note.tags if t not in SUGGESTED_TAGS}


def check_conflicts(note_id: str) -> ConflictReport:
    """Check whether a note contradicts or replaces any other open note.

    This only reports. It never changes or deletes anything. Show the report to the
    boss, and only call supersede_note after they confirm.

    Args:
        note_id: The id of the note to check, usually one that was just saved.
    """
    notes = load_notes()
    new_note = find_note(notes, note_id)
    subjects = _subject_tags(new_note)

    candidates = [
        n
        for n in notes
        if n.id != new_note.id
        and n.status == "open"
        and n.source == new_note.source
        and subjects & _subject_tags(n)
    ][-MAX_COMPARE:]

    if not candidates:
        return ConflictReport()

    existing = "\n".join(f"{n.id}: {n.text}" for n in candidates)
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": CONFLICT_PROMPT},
            {
                "role": "user",
                "content": f"New note: {new_note.text}\n\nExisting notes:\n{existing}",
            },
        ],
        format=ConflictReport.model_json_schema(),
        options={"temperature": TEMPERATURE, "num_ctx": NUM_CTX},
    )

    report = ConflictReport.model_validate_json(response["message"]["content"])
    # Our code checks the ids, since the model can make them up
    valid_ids = {n.id for n in candidates}
    report.conflicts = [c for c in report.conflicts if c.note_id in valid_ids]
    return report


if __name__ == "__main__":
    from tools.notes.save_note import save_note

    # 1. Complete and delete
    todo = save_note(
        "Call Dana about Thursday lunch",
        tags=["dana", "todo"],
        source="secretary",
    )
    print(f"Saved:     {todo.id} ({todo.status})")
    print(f"Completed: {complete_note(todo.id).status}")
    delete_note(todo.id)
    print(f"Deleted. Total notes: {len(load_notes())}")

    # 2. Conflict check
    old = save_note(
        "Dana prefers Thursday lunches",
        tags=["dana", "preference"],
        source="secretary",
    )
    new = save_note(
        "Dana now prefers Tuesday lunches",
        tags=["dana", "preference"],
        source="secretary",
    )
    report = check_conflicts(new.id)
    if report.conflicts:
        for c in report.conflicts:
            print(f"CONFLICT with {c.note_id}: {c.reason}")
    else:
        print("No conflicts found.")

    delete_note(old.id)  # clean up the test notes
    delete_note(new.id)