n = int(input())
count = 0
t = int(input())
for _ in range(n):
    a, b = map(int, input().split())
    if a <= t <= b:
        count += 1
print(count)
