import json
from pathlib import Path

FAVORITES_PATH = Path.home() / ".config" / "mvg-cli" / "favorites.json"


def load() -> dict[str, str]:
    if not FAVORITES_PATH.exists():
        return {}
    return json.loads(FAVORITES_PATH.read_text())


def save(favorites: dict[str, str]) -> None:
    FAVORITES_PATH.parent.mkdir(parents=True, exist_ok=True)
    FAVORITES_PATH.write_text(json.dumps(favorites, indent=2, ensure_ascii=False))


def resolve(name: str) -> str:
    return load().get(name, name)
