from __future__ import annotations
import datetime as _dt
from functools import wraps
from typing import Callable, Any

def function_logger(path: str):
    """Декоратор логирования вызовов функции в файл path."""
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = _dt.datetime.now()
            result = None
            has_result = True
            try:
                result = func(*args, **kwargs)
                if result is None:
                    has_result = False
                return result
            finally:
                end = _dt.datetime.now()
                duration = end - start
                with open(path, "a", encoding="utf-8") as f:
                    f.write(f"{func.__name__}\n")
                    f.write(f"{start}\n")
                    f.write(f"{args if args else ()}\n")
                    f.write(f"{kwargs if kwargs else {}}\n")
                    f.write(f"{result if has_result else '-'}\n")
                    f.write(f"{end}\n")
                    f.write(f"{duration}\n")
        return wrapper
    return decorator
