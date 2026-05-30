"""Задача 4: обработка списка.

process_list переписана через list comprehension.
process_list_gen — генератор с той же логикой.

Сравнение скорости (типично):
- list comprehension обычно быстрее, чем цикл с append.
- генератор экономит память и может быть быстрее при частичном потреблении, но при полном
  превращении в список обычно сопоставим или немного медленнее list comprehension.
"""

from __future__ import annotations
from typing import Iterable, Iterator, List

def process_list(arr: list[int]) -> list[int]:
    return [x * x if x % 2 == 0 else x * x * x for x in arr]

def process_list_gen(arr: Iterable[int]) -> Iterator[int]:
    for x in arr:
        yield x * x if x % 2 == 0 else x * x * x
