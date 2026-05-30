from __future__ import annotations
import math
import random
from typing import Optional

def circle_square_mk(r: float, n: int, rng: Optional[random.Random] = None) -> float:
    """Площадь круга методом Монте-Карло.

    r: радиус
    n: число экспериментов
    rng: опционально random.Random для воспроизводимости в тестах
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if r < 0:
        raise ValueError("r must be non-negative")
    if r == 0:
        return 0.0
    if rng is None:
        rng = random

    inside = 0
    # равномерно по квадрату [-r, r]x[-r, r]
    for _ in range(n):
        x = (rng.random() * 2 - 1) * r
        y = (rng.random() * 2 - 1) * r
        if x * x + y * y <= r * r:
            inside += 1
    square_area = (2 * r) ** 2
    return inside / n * square_area

if __name__ == "__main__":
    # пример: python circle_square_mk.py 1 100000
    import sys
    if len(sys.argv) == 3:
        r = float(sys.argv[1])
        n = int(sys.argv[2])
        est = circle_square_mk(r, n)
        print(est)
        print("formula:", math.pi * r * r)
