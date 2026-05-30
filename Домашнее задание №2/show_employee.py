from __future__ import annotations

def show_employee(name: str, salary: int | float = 100000) -> str:
    """Вернуть строку вида: 'Иванов Иван Иванович: 30000 ₽'."""
    if salary is None:
        salary = 100000
    return f"{name}: {salary} ₽"
