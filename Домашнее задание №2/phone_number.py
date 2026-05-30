from __future__ import annotations
import re

def normalize_digits(s: str) -> str:
    digits = re.sub(r"\D", "", s)
    if len(digits) < 10:
        raise ValueError("phone number must contain at least 10 digits")
    return digits[-10:]

def format_ru_phone(digits10: str) -> str:
    if len(digits10) != 10 or not digits10.isdigit():
        raise ValueError("digits10 must be 10 digits")
    return f"+7 ({digits10[0:3]}) {digits10[3:6]}-{digits10[6:8]}-{digits10[8:10]}"

def wrapper(f):
    def fun(l):
        # сортировка должна быть по числовой части (10 цифр), а не по исходной строке
        digits = [normalize_digits(x) for x in l]
        digits.sort()
        return [format_ru_phone(d) for d in digits]
    return fun

@wrapper
def sort_phone(l):
    # f оставлен для соответствия заготовке; реальную сортировку делает wrapper
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
