from __future__ import annotations
import os
import sys
from collections import defaultdict
from typing import List

def sort_files_by_extension(directory: str) -> list[str]:
    """Список файлов (без каталогов), сгруппированных по расширению и отсортированных."""
    items = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            items.append(name)

    groups = defaultdict(list)
    for name in items:
        ext = os.path.splitext(name)[1]  # включая точку, либо ''
        groups[ext].append(name)

    result = []
    for ext in sorted(groups.keys()):
        for name in sorted(groups[ext]):
            result.append(name)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python files_sort.py <directory>")
    for name in sort_files_by_extension(sys.argv[1]):
        print(name)
