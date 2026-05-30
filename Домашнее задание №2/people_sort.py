from __future__ import annotations
import operator
from typing import List, Sequence

def person_lister(f):
    def inner(people):
        # stable sort by age (index 2)
        people_sorted = sorted(people, key=lambda p: int(p[2]))
        return [f(p) for p in people_sorted]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')
