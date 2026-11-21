import pytest


@pytest.fixture
def notes_file(tmp_path, monkeypatch):
    """Point the notes tools at a temporary file so tests never touch real notes."""
    path = tmp_path / "notes.json"
    monkeypatch.setattr("tools.notes.store.NOTES_FILE", str(path))
    return path