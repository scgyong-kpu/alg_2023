from random import seed, randint
from heapdict import heapdict
from data_city import five_letter_cities, City
from vis import ClusterVisualizer as Visualizer

class Cluster:
  def __init__(self, cities):
    self.cities = cities
    self.dists = heapdict()
    self.centers = []

  def addCenter(self):
    n_cities = len(self.cities)
    if not self.centers:
      # 이번에 추가되는 센터가 최초의 센터이면
      this_center = randint(0, n_cities - 1)
    else:
      return

    # 이번에 추가된 센터를 기록한다
    self.dists[this_center] = (0, this_center)
    self.centers.append(this_center)

    vis.draw()

  # cities 만 남겨두고 재시작한다. 시작 도시를 랜덤하게 선택하기 때문에 다른 답을 구해 본다
  def reset(self):
    self.dists = heapdict()
    self.centers = []

# Random Seed 를 정해 두어 랜덤이 정해진 순서대로 나오도록 한다
seed('cluster')
vis = Visualizer('Clustering')
gen = True
while True:
  if gen:
    # 약 200개까지의 도시를 임의로 선택한다
    beg = randint(0, 700)
    end = randint(beg+15, beg+200)
    cities = five_letter_cities[beg:end]
    # x좌표, y좌표 별로 정렬한다
    cities.sort(key=lambda c: c.x*10000+c.y)
    City.apply_index(cities)
    alg = Cluster(cities)
    vis.setup(alg, False)
    gen = False

  vis.draw()

  # r 을 누를때마다 클러스터가 하나씩 추가된다
  alg.addCenter()
  if not vis.end(): break

  # LeftShift+R 을 하면 도시는 그대로 두고 처음부터 다시
  if vis.restart_rshift:
    alg.reset()

  # RightShift+R 을 하면 도시들을 랜덤하게 다시 생성한다
  if vis.restart_lshift:
    gen = True
