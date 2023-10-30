from collections import defaultdict
from heapq import heappush, heappop

with open('data_knapsack.json') as f:
  contents = f.read()
  print(f'{len(contents)=}')

counts = defaultdict(int)
for ch in contents:
    counts[ch] += 1

print(counts)

class Node:
  def __init__(self, freq, ch, left=None, right=None, code=''):
    self.freq = freq
    self.ch = ch
    self.left = left
    self.right = right
    self.code = code
  def __repr__(self):
    ch = self.ch
    if ch == '\n': ch = '\\n'
    elif ch == '\\': ch = '\\\\'
    s = f'<{self.freq}/{ch}'
    if self.left is not None:
      s += f' L={self.left}'
    if self.right is not None:
      s += f' R={self.right}'
    s += '>'
    return s
  def __lt__(self, other): # 객체를 빈도수로 비교하기위해
    return self.freq < other.freq

nodes = []
for ch in counts:
  node = Node(counts[ch], ch)
  heappush(nodes, node)

print(nodes)

while len(nodes) > 1:
  n1 = heappop(nodes)
  n2 = heappop(nodes)
  node = Node(n1.freq+n2.freq, n1.ch+n2.ch, n1, n2)
  heappush(nodes, node)

print(nodes)

def printTree(node, indent=0):
  print(f'{" " * indent}{node.freq}/{node.ch}')
  if node.left is not None:
    printTree(node.left, indent+2)
  if node.right is not None:
    printTree(node.right, indent+2)

# printTree(nodes[0])

codes = dict()

def assignCode(node):
  if node.left is not None:
    node.left.code = node.code + '0'
    assignCode(node.left)
  if node.right is not None:
    node.right.code = node.code + '1'
    assignCode(node.right)
  if node.left is None and node.right is None: # Leaf
    print(f'{node.ch}({node.freq}):{node.code}', end=' ')
    codes[node.ch] = node.code

assignCode(nodes[0])
print()

def encode():
  ba = bytearray()
  bits = ''
  for ch in contents:
    code = codes[ch]
    bits += code
    while len(bits) >= 8:
      byte, bits = bits[:8], bits[8:]
      ba.append(int(byte, base=2))
  if len(bits) > 0:
    byte = bits + '0' * (8 - len(bits))
    ba.append(int(byte, base=2))
  return ba
ba = encode()
print(ba)
