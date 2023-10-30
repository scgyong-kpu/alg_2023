from collections import defaultdict

with open('data_knapsack.json') as f:
  contents = f.read()
  print(f'{len(contents)=}')

counts = defaultdict(int)
for ch in contents:
    counts[ch] += 1

print(counts)

class Node:
  def __init__(self, freq, ch, left=None, right=None, code=None):
    self.freq = freq
    if ch == '\n': ch = '\\n'
    elif ch == '\\': ch = '\\\\'
    self.ch = ch
    self.left = left
    self.right = right
    self.code = code
  def __repr__(self):
    s = f'<{self.freq}/{self.ch}'
    if self.left is not None:
      s += ' L={self.left}'
    if self.right is not None:
      s += ' R={self.right}'
    s += '>'
    return s
  def __lt__(self, other): # 객체를 빈도수로 비교하기위해
    return self.freq < other.freq

nodes = []
for ch in counts:
  node = Node(counts[ch], ch)
  nodes.append(node)

print('----- Before sort -----')
print(nodes)
nodes.sort()
print('----- After  sort -----')
print(nodes)
