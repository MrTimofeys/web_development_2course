from __future__ import annotations
import os
import sys
from typing import Optional, List

def find_file(start_dir: str, filename: str) -> Optional[str]:
    """Рекурсивный поиск файла по имени. Возвращает путь или None."""
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def first_lines(path: str, n: int = 5) -> list[str]:
    lines = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for _ in range(n):
            line = f.readline()
            if line == "":
                break
            lines.append(line.rstrip("\n"))
    return lines

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python file_search.py <filename>")
    target = sys.argv[1]
    base = os.path.dirname(os.path.abspath(__file__))
    found = find_file(base, target)
    if found is None:
        print(f"Файл {target} не найден")
    else:
        for line in first_lines(found, 5):
            print(line)
