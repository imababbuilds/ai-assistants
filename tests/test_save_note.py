import pytest

from tools.notes.manage_notes import complete_note
from tools.notes.save_note import save_note
from tools.notes.store import load_notes


def test_saves_note_with_expected_fields(notes_file):
    note = save_note("Dana prefers Thursday lunches", tags=["Dana", " preference "], source="secretary")
    assert note.id
    assert note.status == "open"
    assert note.tags == ["dana", "preference"]
    assert len(load_notes()) == 1


def test_empty_note_is_rejected(notes_file):
    with pytest.raises(ValueError):
        save_note("   ")


def test_duplicate_from_same_assistant_is_not_saved_twice(notes_file):
    first = save_note("Call Dana", tags=["todo"], source="secretary")
    second = save_note("  call   dana ", tags=["dana"], source="secretary")
    assert second.id == first.id
    notes = load_notes()
    assert len(notes) == 1
    assert notes[0].tags == ["todo", "dana"]


def test_same_text_from_different_assistants_is_kept_separate(notes_file):
    save_note("Call Dana", source="secretary")
    save_note("Call Dana", source="intern")
    assert len(load_notes()) == 2


def test_completed_note_can_be_saved_again(notes_file):
    first = save_note("Send weekly report", source="secretary")
    complete_note(first.id)
    second = save_note("Send weekly report", source="secretary")
    assert second.id != first.id
    assert len(load_notes()) == 2