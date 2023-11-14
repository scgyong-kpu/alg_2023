from coin_visualizer import CoinChangeVisualizer as Visualizer
from copy import deepcopy

INF = float('inf')

class CoinChange:
  def __init__(self, coins, money):
    self.coins = coins
    self.money = money

    self.n_coin = len(self.coins)
    self.C = [ INF for _ in range(self.money + 2) ]
    self.C[0] = 0
    self.P = [ [] for _ in range(self.money + 2) ]

  def start(self):
    for j in range(1, self.money+1):
      self.P[j] = []
      vis.money(j)
      for i in range(self.n_coin):
        vis.coin(i)
        coin = self.coins[i]
        if coin <= j and self.C[j-coin] + 1 < self.C[j]:
          vis.copy_from(j-coin)
          self.C[j] = self.C[j-coin] + 1
          self.P[j] = deepcopy(self.P[j-coin])   # j원을 새 동전으로 거르스로 남은 액수에 대한 사용된 동전들
          self.P[j].append((i, coin))     # 새 동전 추가
          vis.draw()

    print('Money =', self.money, 'Coin count =', self.C[self.money], 'Coins =', self.P[self.money])

if __name__ == '__main__':
  vis = Visualizer('Coin Change')
  cc = CoinChange([1, 5, 10, 11, 16, 8], 23)
  vis.setup(cc)
  vis.draw()
  cc.start()
  vis.end()