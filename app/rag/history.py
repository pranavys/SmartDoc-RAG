from app.db.models import Message


def format_history(messages: list[Message]) -> str:
    if not messages:
        return ""

    history_parts = []

    for message in messages:
        role = message.role.capitalize()

        history_parts.append(
            f"{role}: {message.content}"
        )

    return "\n".join(history_parts)