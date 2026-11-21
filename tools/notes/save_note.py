from datetime import datetime

from tools.notes.store import Note, load_notes, write_notes


def _normalize(text: str) -> str:
    """Lowercase and collapse spaces, so 'Hi  There' and 'hi there' match."""
    return " ".join(text.lower().split())


def save_note(text: str, tags: list[str] | None = None, source: str = "unknown") -> Note:
    """Save a note so it can be found later.

    If the same assistant already has an open note with the same text, no copy is
    made. Any new tags are added to the existing note, and that note is returned.
    A note that was already completed does not count, so a repeating task can be
    saved again.

    Args:
        text: The note itself.
        tags: Optional short labels. Prefer the suggested tags in config.SUGGESTED_TAGS.
            Add "reminder" when the boss should be told this later, in addition to a
            tag for what it is. Put details (decision, deadline, contact) in the note
            text. Add a lowercase subject tag too, such as a person's name or a project.
        source: The name of the assistant saving the note.
    """
    text = text.strip()
    if not text:
        raise ValueError("Cannot save an empty note.")

    clean_tags = [t.strip().lower() for t in (tags or []) if t.strip()]
    notes = load_notes()

    for existing in notes:
        if (
            existing.status == "open"
            and existing.source == source
            and _normalize(existing.text) == _normalize(text)
        ):
            new_tags = [t for t in clean_tags if t not in existing.tags]
            if new_tags:
                existing.tags.extend(new_tags)
                write_notes(notes)
            return existing

    note = Note(
        text=text,
        created=datetime.now().isoformat(timespec="seconds"),
        tags=clean_tags,
        source=source,
    )
    notes.append(note)
    write_notes(notes)
    return note


if __name__ == "__main__":
    note = save_note(
        "Dana prefers Thursday lunches",
        tags=["Dana", "lunch", "preference"],
        source="secretary",
    )
    print(f"Saved: {note}")
    print(f"Total notes: {len(load_notes())}")