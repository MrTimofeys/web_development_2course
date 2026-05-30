adult, pensioner, child = 0.0, 0.0, 0.0
with open('products.csv', 'r') as f:
    next(f)
    for line in f:
        cat, amt = line.strip().split(',')
        amt = float(amt)
        if cat == 'взрослый':
            adult += amt
        elif cat == 'пенсионер':
            pensioner += amt
        elif cat == 'ребёнок':
            child += amt
print(f"{adult:.2f} {pensioner:.2f} {child:.2f}")
