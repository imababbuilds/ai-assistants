import ollama
from pydantic import BaseModel
from typing import Literal

from config import MODEL, NUM_CTX, TEMPERATURE, MAX_CHARS

SYSTEM_PROMPT = """You are a professional secretary who triages incoming messages for your boss.

Classify each message into exactly one category:
- urgent: needs attention today or has a deadline very soon
- needs_reply: a response is expected, but it is not time-critical
- fyi: informational only, no action needed
- ignore: spam, promotions, or irrelevant

Also give a one-sentence summary and one concrete suggested action.
Only use information that is in the message. Never invent details."""


class Triage(BaseModel):
    category: Literal["urgent", "needs_reply", "fyi", "ignore"]
    summary: str
    suggested_action: str
    truncated: bool = False  


def triage(message: str) -> Triage:
    message = message.strip()

    # Empty input: don't call the model, it would make something up
    if not message:
        return Triage(
            category="ignore",
            summary="Empty message.",
            suggested_action="No action needed.",
        )

    # Oversized input: read what fits, and remember that we cut it
    truncated = len(message) > MAX_CHARS
    if truncated:
        message = message[:MAX_CHARS]

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        format=Triage.model_json_schema(),
        options={"temperature": TEMPERATURE, "num_ctx": NUM_CTX},
    )

    result = Triage.model_validate_json(response["message"]["content"])
    result.truncated = truncated  # overwrite whatever the model put here
    return result


if __name__ == "__main__":
    samples = [
        "From boss: Need the Q3 report by 5pm today.",
        "From Dana: Want to grab lunch sometime next week?",
        "",
        "From Amazon: 50% OFF everything this weekend only!!!",
        "From boss: Please review the attached notes. " + "More details here. " * 2000,
    ]
    for msg in samples:
        result = triage(msg)
        print(f"MESSAGE:  {msg[:80]}")
        print(f"CATEGORY: {result.category}")
        print(f"SUMMARY:  {result.summary}")
        print(f"ACTION:   {result.suggested_action}")
        if result.truncated:
            print("WARNING:  Message was too long, only the first part was read")
        print()