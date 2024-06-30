from functools import wraps
import time
from typing import Any


def set_cooldown(sec, default: Any = None):
    def inner(func):
        loctime = 0
        results = {}

        @wraps(func)
        async def wrapped(*args):
            nonlocal loctime, results
            if loctime > time.time() and args in results:
                return results[args]

            loctime = time.time()+sec

            try:
                result = await func(*args)
            except Exception:
                return default
            else:
                results[args] = result

            return result
        return wrapped
    return inner
