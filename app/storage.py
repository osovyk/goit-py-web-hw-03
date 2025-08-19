import json
from datetime import datetime
import os
from pathlib import Path
from . import BASE_DIR

DATA_DIR = Path(os.environ.get("STORAGE_DIR", BASE_DIR / "storage"))
DATA_FILE = DATA_DIR / "data.json"


def _ensure_store():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def read_all() -> dict:
    _ensure_store()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def append_message(username: str, message: str):
    _ensure_store()
    data = read_all()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data[ts] = {"username": username, "message": message}
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
