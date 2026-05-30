from __future__ import annotations
import sys
from typing import Sequence, Union

def parse_numbers(argv: Sequence[str]) -> list[float]:
    return [float(x) for x in argv]

def sum_from_argv(argv: Sequence[str] | None = None) -> float:
    if argv is None:
        argv = sys.argv[1:]
    nums = parse_numbers(argv)
    return sum(nums)

def format_sum(value: float) -> str:
    # если целое — печатаем без .0
    if value.is_integer():
        return str(int(value))
    return str(value)

if __name__ == "__main__":
    res = sum_from_argv()
    print(format_sum(res))
