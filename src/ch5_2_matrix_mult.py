from vis import MatrixVisualizer
from random import randint

class Matrix:
  def __init__(self, rows, cols, rand=0):
    self.rows, self.cols = rows, cols
    # self.data = []#[ randint(1, 99) for x in range(cols) ] for y in range(rows) ]
    self.data = [ [] for _ in range (rows) ]
    for r in range(rows):
      # self.data.append([])
      for c in range(cols):
        v = randint(1, rand) if rand > 0 else 0
        self.data[r].append(v)

vis = MatrixVisualizer('Matrix Multiplication Visualizer')
rows, common, cols = 3, 4, 2
while True:
  ma = Matrix(rows, common, rand=10)
  mb = Matrix(common, cols, rand=10)
  mc = Matrix(rows, cols)
  vis.start(ma, mb, mc)
  for r in range(mc.rows):
    for c in range(mc.cols):
      for i in range(ma.cols):
        mc.data[r][c] += ma.data[r][i] * mb.data[i][c]
        vis.update(r, c, i)

  again = vis.end()
  if not again: break

  rows = randint(2, 8)
  common = randint(2, 10)
  cols = randint(2, 8)
