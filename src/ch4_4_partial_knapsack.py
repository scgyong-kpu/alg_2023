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
  if cap >= weight_sum + mat['weight']:
    weight_sum += mat['weight']
    price_sum += mat['price']
    items.append(mat)
    print(f'{weight_sum=} {items=}')
  else:
    avail_weight = cap - weight_sum
    if avail_weight > 0:
      price = avail_weight * mat['price'] / mat['weight']
      weight_sum += avail_weight
      price_sum += price
      part = mat.copy()
      part['weight'] = avail_weight
      part['price'] = price
      items.append(part)
      print(f'{weight_sum=} {items=}')
    break
