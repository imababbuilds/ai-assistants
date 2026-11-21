import pytest

from tools.messages.draft_reply import draft_reply
from tools.messages.triage import triage


def test_triage_empty_message_skips_the_model():
    result = triage("   ")
    assert result.category == "ignore"
    assert result.summary == "Empty message."


def test_draft_reply_rejects_empty_message():
    with pytest.raises(ValueError):
        draft_reply("")


def test_draft_reply_rejects_oversized_message():
    with pytest.raises(ValueError):
        draft_reply("x" * 100_000)


@pytest.mark.llm
def test_triage_marks_deadline_from_boss_urgent():
    result = triage("From boss: Need the Q3 report by 5pm today.")
    assert result.category == "urgent"


@pytest.mark.llm
def test_triage_flags_oversized_message_as_truncated():
    result = triage("From boss: " + "More details here. " * 2000)
    assert result.truncated