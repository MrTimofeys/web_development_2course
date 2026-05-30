"""Задача 1: факториал.

Реализованы:
- fact_it: итерационный подсчёт.
- fact_rec: рекурсивный подсчёт через рекурсивное произведение диапазона (product tree),
  что даёт глубину рекурсии O(log n), поэтому подходит для n до 1e5.

Небольшое сравнение скорости (типично, CPython):
- На малых n итерационная версия обычно быстрее из-за меньших накладных расходов.
- На больших n balanced product tree может быть сопоставим или быстрее за счёт более
  выгодного порядка умножений больших целых (зависит от версии Python/платформы).
"""

from __future__ import annotations

def fact_it(n: int) -> int:
    """Итерационный факториал для целого положительного n."""
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 1:
        raise ValueError("n must be >= 1")
    res = 1
    for k in range(2, n + 1):
        res *= k
    return res


def _prod_range(lo: int, hi: int) -> int:
    """Произведение целых чисел на отрезке [lo, hi]. lo<=hi."""
    if lo == hi:
        return lo
    if hi - lo == 1:
        return lo * hi
    mid = (lo + hi) // 2
    return _prod_range(lo, mid) * _prod_range(mid + 1, hi)


def fact_rec(n: int) -> int:
    """Рекурсивный факториал (глубина рекурсии O(log n))."""
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 1:
        raise ValueError("n must be >= 1")
    return _prod_range(1, n)


if __name__ == "__main__":
    import time

    n = 5000
    t0 = time.perf_counter()
    a = fact_it(n)
    t1 = time.perf_counter()
    b = fact_rec(n)
    t2 = time.perf_counter()
    print("fact_it:", t1 - t0)
    print("fact_rec:", t2 - t1)
    print("equal:", a == b)
