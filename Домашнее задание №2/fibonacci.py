from __future__ import annotations

cube = lambda x: x ** 3

def fibonacci(n: int) -> list[int]:
    """Вернуть список первых n чисел Фибоначчи начиная с 0."""
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 1:
        raise ValueError("n must be >= 1")
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))
