import datetime
import functools
import os


def log_action(func):
    """Logs every library action with a timestamp to data/library.log."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs("data", exist_ok=True)
        with open("data/library.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {func.__name__}\n")
        return result
    return wrapper
