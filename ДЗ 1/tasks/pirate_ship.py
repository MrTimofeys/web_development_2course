# Это задача на фракционную 0/1 knapsack (DP), сложная. Пример простого greedy по стоимости/весу:
n, m = map(int, input().split())
items = []
for _ in range(m):
    name, w, c = input().split()
    items.append((name, float(w), float(c)))
items.sort(key=lambda x: x[2]/x[1], reverse=True)
used_w = 0
for name, w, c in items:
    if used_w + w <= n:
        print(f"{name} {w:.2f} {c:.2f}")
        used_w += w
    else:
        frac_w = n - used_w
        frac_c = frac_w * (c / w)
        print(f"{name} {frac_w:.2f} {frac_c:.2f}")
        break
