with open('data_knapsack.json') as f:
  contents = f.read()
  print(f'{len(contents)=}')

counts = dict()
for ch in contents:
  if ch in counts:
    counts[ch] += 1
  else:
    counts[ch] = 1

print(counts)
