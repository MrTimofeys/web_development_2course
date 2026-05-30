from __future__ import annotations

def my_sum(*args: float) -> float:
    """Сумма произвольного количества чисел."""
    total = 0.0
    for x in args:
        total += x
    return total
