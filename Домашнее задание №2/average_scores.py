from __future__ import annotations
from typing import Iterable, Sequence, Tuple, List

def compute_average_scores(scores: Sequence[Sequence[float]]) -> tuple[float, ...]:
    """scores: список из X кортежей/списков длины N (оценки по предметам).
    Возвращает кортеж из N средних значений (по студентам).
    """
    if not scores:
        return tuple()
    # zip(*) даёт по студентам
    avgs = []
    for student_marks in zip(*scores):
        avgs.append(sum(student_marks) / len(student_marks))
    return tuple(avgs)

if __name__ == "__main__":
    n, x = map(int, input().split())
    subjects = []
    for _ in range(x):
        # допускаем вещественные оценки
        subjects.append(tuple(map(float, input().split())))
    for avg in compute_average_scores(subjects):
        print(f"{avg:.1f}")
