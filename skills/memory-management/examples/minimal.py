"""Minimal example: Memory Management (Ch 8). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    state['user_city'] = 'Paris'  # output_key or tool write
    greeting = run('Greet for Paris')
    recall = store.search(('prefs', user_id))


if __name__ == "__main__":
    print(main())
