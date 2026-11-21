import pytest

from tools.notes.manage_notes import complete_note, delete_note, supersede_note
from tools.notes.save_note import save_note
from tools.notes.store import load_notes


def test_complete_keeps_the_note(notes_file):
    note = save_note("Call Dana", source="secretary")
    complete_note(note.id)
    notes = load_notes()
    assert len(notes) == 1
    assert notes[0].status == "done"


def test_supersede_keeps_the_note(notes_file):
    note = save_note("Dana prefers Thursdays", source="secretary")
    supersede_note(note.id)
    assert load_notes()[0].status == "superseded"


def test_delete_removes_the_note(notes_file):
    note = save_note("Call Dana", source="secretary")
    delete_note(note.id)
    assert load_notes() == []


def test_unknown_id_raises(notes_file):
    with pytest.raises(ValueError):
        complete_note("does-not-exist")