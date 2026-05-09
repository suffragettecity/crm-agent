"""
In-memory conversation store, keyed by user/chat ID.
For production, swap the dict for Redis:
  pip install redis
  import redis; r = redis.Redis; r.set(ley, json.dumps(history))
"""
from config.settings import MAX_HISTORY_MESSAGES

_store: dict[str, list[dict]] = {}

def get_history(user_id: str | int) -> list[dict]:
    return _store.get(str(user_id), [])

def save_history(user_id: str | int, history: list[dict]) -> None:
    # keep only the last n messages to avoid ballooning context
    _store[str(user_id)] = history[-MAX_HISTORY_MESSAGES:]

def clear_history(user_id: str | int) -> None:
    _store.pop(str(user_id), None)