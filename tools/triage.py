import ollama
from pydantic import BaseModel
from typing import Literal

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """You are a professional secretary who triages incoming messages for your boss.

Classify each message into exactly one category:
- urgent: needs attention today or has a deadline very soon
- needs_reply: a response is expected, but it is not time-critical
- fyi: informational only, no action needed
- ignore: spam, promotions, or irrelevant

Also give a one-sentence summary and one concrete suggested action."""


class Triage(BaseModel):
    category: Literal["urgent", "needs_reply", "fyi", "ignore"]
    summary: str
    suggested_action: str


def triage(message: str) -> Triage:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        format=Triage.model_json_schema(),
        options={"temperature": 0},
    )
    return Triage.model_validate_json(response["message"]["content"])


if __name__ == "__main__":
    samples = [
        "From boss: Need the Q3 report by 5pm today.",
        "From Dana: Want to grab lunch sometime next week?",
        "From Netflix: Your monthly statement is available.",
        "From Amazon: 50% OFF everything this weekend only!!!",
    ]
    for msg in samples:
        result = triage(msg)
        print(f"MESSAGE:  {msg}")
        print(f"CATEGORY: {result.category}")
        print(f"SUMMARY:  {result.summary}")
        print(f"ACTION:   {result.suggested_action}")
        print()