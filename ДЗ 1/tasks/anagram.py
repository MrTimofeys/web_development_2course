s1, s2 = input().strip(), input().strip()
print("YES" if sorted(s1.lower()) == sorted(s2.lower()) else "NO")
