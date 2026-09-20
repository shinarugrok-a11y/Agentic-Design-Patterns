"""Minimal example: Inter-Agent Communication (A2A) (Ch 15). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    card = fetch_card("http://weather/a2a")  # skills, auth
    task = sendTask(card.url, {"text": "Forecast Paris?"})
    return stream_or_poll(task.id)


if __name__ == "__main__":
    print(main())
