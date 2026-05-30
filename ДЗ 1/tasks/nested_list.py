n = int(input())
students = []

for _ in range(n):
    name = input()
    score = float(input())
    students.append([name, score])

# ✅ ПРАВИЛЬНАЯ ЛОГИКА: ВТОРАЯ ПО УБЫВАНИЮ (НЕ НОЖАЙШАЯ!)
scores = sorted([score for name, score in students])[1]  # ВСЁ!

# Студенты с этой оценкой
names = sorted([name for name, score in students if score == scores])

for name in names:
    print(name)
