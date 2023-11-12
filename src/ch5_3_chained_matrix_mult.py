from vis import ChainedMatrixVisualizer as Visualizer
from random import randint, seed, shuffle

class ChainedMatrixMult:
  def __init__(self, sizes=None):
    if sizes == None:
      sizes = []
      count = randint(5, 10)
      for i in range(count):
        sizes.append(randint(3, 20))
    self.sizes = sizes
    self.matrix_count = len(sizes) - 1
    self.C = [[ 0 for _ in range(self.matrix_count + 1) ] for _ in range(self.matrix_count + 1) ]
    self.P = [[ 0 for _ in range(self.matrix_count + 1) ] for _ in range(self.matrix_count + 1) ]

  def main(self):
    vis.start_all_candidates()

if __name__ == '__main__':
  # seed('Hello')
  vis = Visualizer('Chained Matrix Multiplication')
  cmm = ChainedMatrixMult([2,8,2,9,8,2])
  vis.setup(cmm)
  cmm.main()
  vis.end()
