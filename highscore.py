"""High score persistence using a JSON file."""
import json
import os

_SCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.json")


def load_high_score() -> int:
    """Load the high score from disk. Returns 0 if not found or corrupt."""
    try:
        with open(_SCORE_FILE, "r") as f:
            data = json.load(f)
            return int(data.get("high_score", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, KeyError):
        return 0


def save_high_score(score: int) -> None:
    """Persist the high score to disk."""
    try:
        with open(_SCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)
    except OSError:
        pass  # silently ignore write failures (read-only FS, etc.)
