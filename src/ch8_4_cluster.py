from random import seed, randint
from heapdict import heapdict
from math import sqrt
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

    # 모든 점에 대해 거리갱신을 (필요하면) 합니다
    for i in range(n_cities):
      # 방금 추가된 센터까지의 거리를 구해서
      d = self.distance_between(this_center, i)
      # dists 딕셔너리에 갱신해준다
      if not i in self.dists or d < -self.dists[i][0]:
        self.dists[i] = (-d, this_center)
        # Min-Heap 이므로 음수로 기록해야 최대값을 얻을 수 있으며, 가까운 센터가 어디인지도 함께 저장한다

      # 각 점들에 대해 갱신하는 과정을 보여주자
      vis.compare(i, this_center,
        d if this_center != self.dists[i][1] else 0)

    vis.draw()

  # i1 번째 도시와 i2 번째 도시 사이의 거리를 구한다
  def distance_between(self, i1, i2):
    if i1 >= len(self.cities) or i2 >= len(self.cities):
      print(f'{i1=} {i2=} {len(self.cities)=}')
    c1, c2 = self.cities[i1], self.cities[i2]
    return sqrt((c1.x-c2.x)**2+(c1.y-c2.y)**2)

  # cities 만 남겨두고 재시작한다. 시작 도시를 랜덤하게 선택하기 때문에 다른 답을 구해 본다
  def reset(self):
    self.dists = heapdict()
    self.centers = []

# Random Seed 를 정해 두어 랜덤이 정해진 순서대로 나오도록 한다
seed('K cluster')
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
    vis.setup(alg, True)
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
