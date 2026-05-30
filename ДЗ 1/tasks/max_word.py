import re
with open('example.txt', 'r', encoding='utf-8') as f:
    text = f.read()
words = re.findall(r'\b\w+\b', text.lower())
max_len = max(len(w) for w in words)
max_words = [w.capitalize() for w in words if len(w) == max_len]
for w in max_words:
    print(w)
