n = int(input())
arr = list(map(int, input().split()))

# Убираем дубликаты, сортируем по убыванию
unique_scores = sorted(set(arr), reverse=True)

# Выводим ВТОРУЮ максимальную (индекс 1)
if len(unique_scores) >= 2:
    print(unique_scores[1])
else:
    print(unique_scores[0])  # Если только одно число
