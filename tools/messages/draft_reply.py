import re

import ollama
from pydantic import BaseModel

from config import MODEL, NUM_CTX, DRAFT_TEMPERATURE, MAX_CHARS

SYSTEM_PROMPT = """You draft email replies for the user. The user will read, edit and send your draft, so write in the first person as the user ("I", "my"), never as a third party or assistant.

Rules:
- The incoming message is addressed to the user. Reply to its sender.
- If the user gives instructions about what to say, follow them exactly.
- If there are no instructions, write a neutral reply that only acknowledges the message. Do not claim progress, problems, delays or abilities, and do not agree to anything the message does not ask for. If you would need to know more, ask a short question or use a placeholder.
- Invitations and requests for the user's time or work are decisions. Do not accept or decline them. Use a placeholder so the user can decide.
- Match the sender's tone: casual message gets a casual reply, formal gets formal.
- Keep it short: 1 to 3 sentences. No filler such as "Thank you for the reminder" or "I hope this finds you well".
- Never invent facts, dates, times or commitments. If the user must decide something (a time, a yes or no), put a placeholder in square brackets, like [day/time].
- subject: start with "Re:"

Examples:
Message: From Priya: Are you free to look over the slides tomorrow?
Body: Hi Priya, thanks for asking. [accept or decline, and a time]

Message: From manager: Team meeting moved to 3pm.
Body: Got it, see you at 3.

Message: From manager: I need the budget numbers by Friday.
Body: Understood, I'll get them to you by Friday.

Message: From Sam: Can you send me the invoice?
User instructions: say I'll send it tomorrow
Body: Hi Sam, I'll send it over tomorrow."""


class Draft(BaseModel):
    subject: str
    body: str
    needs_review: bool = False  # set by our code, not the model


def draft_reply(message: str, instructions: str = "") -> Draft:
    message = message.strip()

    if not message:
        raise ValueError("Cannot draft a reply to an empty message.")
    if len(message) > MAX_CHARS:
        raise ValueError("Message is too long to draft a reply safely.")

    user_content = f"Message: {message}"
    if instructions.strip():
        user_content += f"\nUser instructions: {instructions.strip()}"

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        format=Draft.model_json_schema(),
        options={"temperature": DRAFT_TEMPERATURE, "num_ctx": NUM_CTX},
    )

    draft = Draft.model_validate_json(response["message"]["content"])
    # Our code decides this, not the model: does the body contain a [placeholder]?
    draft.needs_review = bool(re.search(r"\[.+?\]", draft.body))
    return draft


if __name__ == "__main__":
    samples = [
        ("From boss: Need the Q3 report by 5pm today.", ""),
        ("From boss: Need the Q3 report by 5pm today.", "tell him it's done and I'll send it at 3"),
        ("From Dana: Want to grab lunch sometime next week?", ""),
        ("From Dana: Want to grab lunch sometime next week?", "say yes, Thursday works"),
        ("From Lee: Can you send me last month's expense report?", ""),
    ]
    for msg, instructions in samples:
        draft = draft_reply(msg, instructions)
        print(f"MESSAGE:      {msg}")
        if instructions:
            print(f"INSTRUCTIONS: {instructions}")
        print(f"SUBJECT:      {draft.subject}")
        print(f"BODY:\n{draft.body}")
        if draft.needs_review:
            print("REVIEW:       Contains placeholders the user needs to fill in")
        print()