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
    vis.start()
    count = self.matrix_count                # 행열은 모두 count 개 이다
    for sub_mult_count in range(2, 2 + 1):   # 일단 부분분제의 크기가 2개 일 때만 해 본다
      vis.sub(sub_mult_count)
      max_start = count - sub_mult_count + 1 # 부분문제 크기가 커지면 시작위치가 제한된다
      for start in range(1, max_start + 1):  # 부분문제의 시작위치를 변경시키며 계산한다
        end = start + sub_mult_count - 1 # inclusive end
        vis.range(start, end)
        self.C[start][end] = float('inf')    # start~end 까지의 횟수를 inf 로 초기화한다
        for k in range(start, end):
          temp = self.C[start][k] + self.C[k+1][end] + self.sizes[start-1]*self.sizes[k]*self.sizes[end]
          # 곱셈을 해당 부분에 넣었을 때 이득이 있는지 확인한다
          vis.compare(k, self.C[start][end] > temp)
          if self.C[start][end] > temp:
            self.C[start][end] = temp        # start~end 까지의 횟수가 몇번인지 저장한다
            self.P[start][end] = k           # 마지막 곱셈을 어디서 해야 하는지 저장한다
            vis.update()

if __name__ == '__main__':
  # seed('Hello')
  vis = Visualizer('Chained Matrix Multiplication')
  cmm = ChainedMatrixMult([2,8,2,9,8,2])
  while True:
    vis.setup(cmm)
    cmm.main()
    again = vis.end()
    if not again: break
    if not vis.restart_lshift:
      cmm = ChainedMatrixMult()
