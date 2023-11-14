from ks_visualizer import KnapsackVisualizer
from copy import deepcopy

class Knapsack:
  def __init__(self, weights, values, capacity):
    self.W = weights
    self.V = values
    self.N = len(weights)
    self.capacity = capacity

    self.K = [[-1 for _ in range(capacity+1)] for _ in range(self.N)]
    self.P = [[[] for _ in range(capacity+1)] for _ in range(self.N)]


  def start(self):
    N, capacity = self.N, self.capacity
    W, V, K, P = self.W, self.V, self.K, self.P

    for w in range(capacity+1):
      self.K[0][w] = 0
      vis.prepare(0, w, True)
    for i in range(N):
      self.K[i][0] = 0
      vis.prepare(i, 0, True)

    for i in range(1, N):
      for w in range(1, capacity+1):
        vis.prepare(i, w)
        if W[i] > w:
          vis.copy_from(i-1, w)
          K[i][w] = K[i-1][w] 
          P[i][w] = P[i-1][w][:]  # item 리스트 복사
        else:
          vis.compare()
          if K[i-1][w] > K[i-1][w - W[i]] + V[i]:
            vis.copy_from(i-1, w)
            K[i][w] = K[i-1][w]
            P[i][w] = deepcopy(P[i-1][w])  # item 리스트 복사
          else:
            vis.copy_from(i-1, w-W[i], i)
            K[i][w] = max(K[i-1][w], K[i-1][w - W[i]] + V[i])  
            P[i][w] = deepcopy(P[i-1][w - W[i]])  # item 리스트 복사
            P[i][w].append(i)  # item 리스트에 item i 추가

    vis.prepare(N)

    print(K[i])    

    print('최대 가치:', K[N-1][capacity])
    print('item 리스트:', P[N-1][capacity])

if __name__ == '__main__':
  vis = KnapsackVisualizer('0-1 Knapsack')
  weights = [0,  5,  4,  6,  3]  # item 1..4의 무게, 0은 제외
  values  = [0, 10, 40, 30, 50]  # item 1..4의 가치, 0은 제외
  capacity = 10                  # 배낭의 용량

  ks = Knapsack(weights, values, capacity)
  vis.setup(ks)
  vis.draw()
  ks.start()
  vis.end()