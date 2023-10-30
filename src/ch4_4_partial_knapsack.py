import json
with open('data_knapsack.json') as f:
  mats = json.load(f)
print(f'Before: {mats=}')
mats.sort(key=lambda m:m['price']/m['weight'], reverse=True)
print(f'After : {mats=}')

cap = 85
items = []
weight_sum = 0
price_sum = 0

for mat in mats:
    weight_sum += mat['weight']
    price_sum += mat['price']
    items.append(mat)
    print(f'{weight_sum=} {items=}')
